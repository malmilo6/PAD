const redis = require('redis');
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const axios = require('axios');
const rateLimit = require('express-rate-limit');
const loadBalancerUrl = 'http://nginx_load_balancer'; // Point to the load balancer
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer();
const app = express();
const PORT = process.env.PORT || 3000;

// Create a Redis client
const redisClient = redis.createClient({
    url: 'redis://redis:6379', // Adjust to match your Redis service
});

redisClient.connect().catch((err) => {
    console.error("Redis connection error:", err);
});

// Concurent task limiter
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 1000000, // limit each IP up to 100 reqs
    message: "Too many requests, please try again later.",
});

app.use(limiter);


// Cache middleware
const cacheMiddleware = async (req, res, next) => {
    const cacheKey = req.originalUrl; // Use the request URL as the cache key

    try {
        // Check Redis for cached data
        const cachedData = await redisClient.get(cacheKey);

        if (cachedData) {
            console.log('Serving from cache for:', cacheKey);
            return res.status(200).json(JSON.parse(cachedData)); // Return cached response
        } else {
            next();
        }
    } catch (err) {
        console.error('Redis error:', err);
        next();
    }
};

// Proxy for Weather Data Service

app.use('/api/v1/health_wds', createProxyMiddleware({
    target: 'http://django-weather-data-service:8000',
    changeOrigin: true,
}));

// // Proxy for User Alert Service
// app.use('/api/v1/health_uas', createProxyMiddleware({
//     target: 'http://django-user-alert-service:8001',
//     changeOrigin: true,
// }));

app.use('/api/v1/current-weather', cacheMiddleware, async (req, res) => {
    const cacheKey = req.originalUrl;

    try {
        const response = await axios.get('http://django-user-alert-service:8001' + req.originalUrl);

        // Cache
        await redisClient.setEx(cacheKey, 60, JSON.stringify(response.data));

        res.status(200).json(response.data);
    } catch (error) {
        console.error('Error fetching health data:', error);
        res.status(500).json({ error: 'Unable to fetch health data' });
    }
});


// app.use('/api/v1/weather-prediction', cacheMiddleware, async (req, res) => {
//     const cacheKey = req.originalUrl;
//
//     try {
//         const response = await axios.get('http://django-user-alert-service:8001' + req.originalUrl);
//
//         // Cache
//         await redisClient.setEx(cacheKey, 60, JSON.stringify(response.data));
//
//         res.status(200).json(response.data);
//     } catch (error) {
//         console.error('Error fetching health data:', error);
//         res.status(500).json({ error: 'Unable to fetch health data' });
//     }
// });

app.get('/api/v1/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

async function postOnStart() {
  const anotherServiceUrl = 'http://service_discovery:5000/register';
  const payload = {
    name: 'gateway',
    ip: '127.0.0.1',
    port: '3000',
  };

  try {
    const response = await axios.post(anotherServiceUrl, payload);
    if (response.status === 200) {
      console.log('Successfully registered with the other service.');
    } else {
      console.error(`Failed to register with the other service. Status code: ${response.status}`);
    }
  } catch (error) {
    console.error(`Error registering with the other service: ${error.message}`);
  }
}

app.use((req, res) => {
  // Log the incoming request
  console.log(`Received request for: ${req.url}`);

  // Forward the request to the load balancer
  proxy.web(req, res, { target: loadBalancerUrl }, (error) => {
    console.error(`Error proxying request to ${loadBalancerUrl}:`, error);
    res.status(500).send('An error occurred while forwarding the request.');
  });
});


app.listen(PORT, () => {
    console.log(`Gateway listening on port ${PORT}`);
    postOnStart();
});
