CREATE TABLE `users` (
    `id` varchar(255) NOT NULL,
    `username` varchar(50) NOT NULL,
    `email` varchar(100) NOT NULL,
    `phone` varchar(20) DEFAULT NULL,
    `password_hash` varchar(255) DEFAULT NULL,
    `telegram_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `chat_id` varchar(50) DEFAULT NULL,
    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
)

CREATE TABLE `otp_tokens` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` varchar(255) DEFAULT NULL,
    `otp_code` varchar(6) DEFAULT NULL,
    `expires_at` datetime DEFAULT NULL,
    `is_used` tinyint(1) DEFAULT '0',
    PRIMARY KEY (`id`),
    KEY `user_id` (`user_id`),
    CONSTRAINT `otp_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
)