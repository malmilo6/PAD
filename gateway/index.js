const redis = require('redis');
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const axios = require('axios');
const rateLimit = require('express-rate-limit');

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
    max: 100, // limit each IP up to 100 reqs
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

// Proxy for User Alert Service
app.use('/api/v1/health_uas', createProxyMiddleware({
    target: 'http://django-user-alert-service:8001',
    changeOrigin: true,
}));

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


app.use('/api/v1/weather-prediction', cacheMiddleware, async (req, res) => {
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

app.listen(PORT, () => {
    console.log(`Gateway listening on port ${PORT}`);
});
