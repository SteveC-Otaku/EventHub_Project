/*
 Navicat Premium Data Transfer

 Source Server         : aaa
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : eventhub_db

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 06/06/2025 12:46:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for events
-- ----------------------------
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `general_price` double NOT NULL DEFAULT 0,
  `general_capacity` int NOT NULL DEFAULT 0,
  `general_remaining` int NOT NULL DEFAULT 0,
  `vip_price` double NOT NULL DEFAULT 0,
  `vip_capacity` int NOT NULL DEFAULT 0,
  `vip_remaining` int NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `organizer_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_events_organizer_id`(`organizer_id` ASC) USING BTREE,
  CONSTRAINT `fk_events_organizer` FOREIGN KEY (`organizer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 54 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of events
-- ----------------------------
INSERT INTO `events` VALUES (1, 'Tech Conference 2024', 'Join us for the biggest tech conference of the year. Learn from industry experts and network with professionals.', '2023-12-15', '09:00:00', 'Convention Center, New York', 'images/tech_conference_2023.jpg', 'conference', 50, 500, 350, 150, 100, 75, '2025-06-04 14:10:47', 1);
INSERT INTO `events` VALUES (2, 'Summer Music Festival', 'A three-day music festival featuring top artists from around the world. Food, drinks, and camping available.', '2023-07-20', '14:00:00', 'Central Park, New York', 'images/summer_music_festival.jpg', 'concert', 75, 2000, 1197, 250, 300, 150, '2025-06-04 14:10:47', 2);
INSERT INTO `events` VALUES (3, 'Business Networking Lunch', 'Connect with local business leaders and entrepreneurs over lunch. Great opportunity for networking and collaboration.', '2023-06-10', '12:00:00', 'Grand Hotel, Boston', 'images/business_networking_lunch.jpg', 'networking', 30, 100, 65, 75, 20, 10, '2025-06-04 14:10:47', 3);
INSERT INTO `events` VALUES (4, 'Web Development Workshop', 'Learn the latest web development techniques and tools in this hands-on workshop. Suitable for beginners and intermediate developers.', '2023-08-05', '10:00:00', 'Tech Hub, San Francisco', 'images/web_development_workshop.jpg', 'workshop', 25, 50, 29, 60, 10, 5, '2025-06-04 14:10:47', 4);
INSERT INTO `events` VALUES (5, 'Startup Pitch Competition', 'Watch innovative startups pitch their ideas to a panel of investors. Networking reception to follow.', '2023-09-20', '18:00:00', 'Innovation Center, Austin', 'images/startup_pitch_competition.jpg', 'networking', 15, 200, 120, 50, 30, 15, '2025-06-04 14:10:47', 5);
INSERT INTO `events` VALUES (6, 'AI and Machine Learning Conference', 'Explore the latest advancements in artificial intelligence and machine learning with leading researchers and practitioners.', '2023-11-10', '09:30:00', 'Science Center, Seattle', 'images/ai_machine_learning_conference.jpg', 'conference', 60, 300, 200, 180, 50, 30, '2025-06-04 14:10:47', 1);
INSERT INTO `events` VALUES (54, 'Startup Pitch Competition 2023', 'Experience the latest in workshop held at Riverside Pavilion, Miami.', '2025-07-06', '16:39:00', 'Riverside Pavilion, Miami', 'images/web_development_workshop.jpg', 'workshop', 25, 300, 300, 37, 75, 75, '2025-06-06 04:44:50', 1);
INSERT INTO `events` VALUES (55, 'Blockchain Meetup 2023', 'A must-attend networking for professionals, hosted at Science Center, Seattle.', '2025-10-04', '12:08:00', 'Science Center, Seattle', 'images/healthcare_innovation_forum.jpg', 'networking', 75, 500, 500, 187, 250, 250, '2025-06-06 04:44:50', 2);
INSERT INTO `events` VALUES (56, 'Blockchain Meetup 2023', 'Experience the latest in workshop held at Science Center, Seattle.', '2026-01-03', '04:10:00', 'Science Center, Seattle', 'images/web_development_workshop.jpg', 'workshop', 75, 300, 300, 112, 75, 75, '2025-06-06 04:44:50', 23);
INSERT INTO `events` VALUES (57, 'Startup Pitch Competition 2023', 'Connect and learn at our concert in Convention Center, New York.', '2025-10-23', '22:37:00', 'Convention Center, New York', 'images/startup_pitch_competition.jpg', 'concert', 40, 500, 500, 60, 250, 250, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (58, 'Business Networking Lunch 2023', 'An unforgettable workshop experience, happening at Tech Hub, San Francisco.', '2026-02-05', '20:21:00', 'Tech Hub, San Francisco', 'images/film_media_expo.jpg', 'workshop', 60, 200, 200, 150, 40, 40, '2025-06-06 04:44:50', 21);
INSERT INTO `events` VALUES (59, 'Startup Pitch Competition 2023', 'An unforgettable networking experience, happening at Convention Center, New York.', '2026-04-21', '10:59:00', 'Convention Center, New York', 'images/summer_music_festival.jpg', 'networking', 100, 500, 500, 150, 250, 250, '2025-06-06 04:44:50', 21);
INSERT INTO `events` VALUES (60, 'Film & Media Expo 2023', 'Connect and learn at our concert in Tech Hub, San Francisco.', '2025-12-03', '09:58:00', 'Tech Hub, San Francisco', 'images/tech_conference_2023.jpg', 'concert', 60, 100, 100, 120, 25, 25, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (61, 'Tech Conference 2023', 'Experience the latest in workshop held at Tech Hub, San Francisco.', '2026-05-13', '15:16:00', 'Tech Hub, San Francisco', 'images/web_development_workshop.jpg', 'workshop', 75, 100, 100, 112, 25, 25, '2025-06-06 04:44:50', 21);
INSERT INTO `events` VALUES (62, 'Tech Conference 2023', 'Don\'t miss this exclusive workshop at Downtown Arena, Los Angeles.', '2025-07-04', '01:27:00', 'Downtown Arena, Los Angeles', 'images/business_networking_lunch.jpg', 'workshop', 50, 200, 200, 100, 40, 40, '2025-06-06 04:44:50', 29);
INSERT INTO `events` VALUES (63, 'Tech Conference 2024', 'Don\'t miss this exclusive concert at Downtown Arena, Los Angeles.', '2025-10-27', '17:55:00', 'Downtown Arena, Los Angeles', 'images/blockchain_meetup.jpg', 'concert', 30, 1000, 1000, 75, 250, 250, '2025-06-06 04:44:50', 4);
INSERT INTO `events` VALUES (64, 'Film & Media Expo 2024', 'Join us for the biggest conference of the year in Downtown Arena, Los Angeles.', '2025-07-09', '09:47:00', 'Downtown Arena, Los Angeles', 'images/startup_pitch_competition.jpg', 'conference', 20, 100, 100, 30, 33, 33, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (65, 'Business Networking Lunch 2024', 'Join us for the biggest networking of the year in Downtown Arena, Los Angeles.', '2025-10-16', '00:04:00', 'Downtown Arena, Los Angeles', 'images/startup_pitch_competition.jpg', 'networking', 40, 300, 300, 100, 100, 100, '2025-06-06 04:44:50', 5);
INSERT INTO `events` VALUES (66, 'Healthcare Innovation Forum 2024', 'Join us for the biggest workshop of the year in Tech Hub, San Francisco.', '2025-06-10', '13:21:00', 'Tech Hub, San Francisco', 'images/business_networking_lunch.jpg', 'workshop', 50, 50, 50, 75, 16, 16, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (67, 'Summer Music Festival 2024', 'Experience the latest in workshop held at City Conference Hall, Denver.', '2025-06-27', '21:32:00', 'City Conference Hall, Denver', 'images/summer_music_festival.jpg', 'workshop', 20, 1000, 1000, 50, 200, 200, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (68, 'Digital Marketing Seminar 2024', 'An unforgettable concert experience, happening at Tech Hub, San Francisco.', '2026-03-07', '21:36:00', 'Tech Hub, San Francisco', 'images/film_media_expo.jpg', 'concert', 75, 50, 50, 150, 12, 12, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (69, 'Summer Music Festival 2024', 'An unforgettable workshop experience, happening at Riverside Pavilion, Miami.', '2025-09-19', '06:25:00', 'Riverside Pavilion, Miami', 'images/digital_marketing_seminar.jpg', 'workshop', 100, 200, 200, 200, 66, 66, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (70, 'Blockchain Meetup 2024', 'An unforgettable concert experience, happening at Convention Center, New York.', '2025-08-30', '14:16:00', 'Convention Center, New York', 'images/healthcare_innovation_forum.jpg', 'concert', 25, 50, 50, 37, 16, 16, '2025-06-06 04:44:50', 28);
INSERT INTO `events` VALUES (71, 'Startup Pitch Competition 2024', 'Experience the latest in conference held at Convention Plaza, Dallas.', '2025-11-20', '23:25:00', 'Convention Plaza, Dallas', 'images/tech_conference_2023.jpg', 'conference', 50, 200, 200, 75, 40, 40, '2025-06-06 04:44:50', 22);
INSERT INTO `events` VALUES (72, 'Startup Pitch Competition 2025', 'Join us for the biggest workshop of the year in Expo Hall, Chicago.', '2025-11-20', '13:39:00', 'Expo Hall, Chicago', 'images/tech_conference_2023.jpg', 'workshop', 30, 50, 50, 45, 10, 10, '2025-06-06 04:44:50', 4);
INSERT INTO `events` VALUES (73, 'Web Development Workshop 2025', 'Connect and learn at our conference in Convention Center, New York.', '2026-02-27', '00:39:00', 'Convention Center, New York', 'images/film_media_expo.jpg', 'conference', 30, 500, 500, 60, 125, 125, '2025-06-06 04:44:50', 22);
INSERT INTO `events` VALUES (74, 'Healthcare Innovation Forum 2025', 'Join us for the biggest networking of the year in Grand Hotel, Boston.', '2026-02-03', '10:25:00', 'Grand Hotel, Boston', 'images/tech_conference_2023.jpg', 'networking', 25, 1000, 1000, 37, 250, 250, '2025-06-06 04:44:50', 24);
INSERT INTO `events` VALUES (75, 'Tech Conference 2025', 'Join us for the biggest conference of the year in University Auditorium, Atlanta.', '2025-07-28', '00:26:00', 'University Auditorium, Atlanta', 'images/healthcare_innovation_forum.jpg', 'conference', 100, 200, 200, 200, 50, 50, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (76, 'Digital Marketing Seminar 2025', 'An unforgettable concert experience, happening at Expo Hall, Chicago.', '2026-01-02', '08:10:00', 'Expo Hall, Chicago', 'images/summer_music_festival.jpg', 'concert', 25, 200, 200, 62, 40, 40, '2025-06-06 04:44:50', 23);
INSERT INTO `events` VALUES (77, 'Summer Music Festival 2025', 'A must-attend concert for professionals, hosted at Convention Plaza, Dallas.', '2025-11-17', '12:11:00', 'Convention Plaza, Dallas', 'images/ai_machine_learning_conference.jpg', 'concert', 25, 100, 100, 50, 20, 20, '2025-06-06 04:44:50', 24);
INSERT INTO `events` VALUES (78, 'Digital Marketing Seminar 2025', 'Experience the latest in concert held at University Auditorium, Atlanta.', '2026-05-27', '02:57:00', 'University Auditorium, Atlanta', 'images/tech_conference_2023.jpg', 'concert', 40, 1000, 1000, 100, 200, 200, '2025-06-06 04:44:50', 22);
INSERT INTO `events` VALUES (79, 'Startup Pitch Competition 2025', 'A must-attend networking for professionals, hosted at University Auditorium, Atlanta.', '2025-12-25', '14:38:00', 'University Auditorium, Atlanta', 'images/digital_marketing_seminar.jpg', 'networking', 25, 100, 100, 50, 33, 33, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (80, 'Digital Marketing Seminar 2025', 'A must-attend conference for professionals, hosted at Expo Hall, Chicago.', '2026-06-02', '07:16:00', 'Expo Hall, Chicago', 'images/tech_conference_2023.jpg', 'conference', 20, 1000, 1000, 30, 250, 250, '2025-06-06 04:44:50', 27);
INSERT INTO `events` VALUES (81, 'Healthcare Innovation Forum 2025', 'Don\'t miss this exclusive conference at Central Park, New York.', '2025-07-26', '18:19:00', 'Central Park, New York', 'images/tech_conference_2023.jpg', 'conference', 25, 100, 100, 37, 33, 33, '2025-06-06 04:44:50', 28);
INSERT INTO `events` VALUES (82, 'Business Networking Lunch 2026', 'Don\'t miss this exclusive networking at Convention Center, New York.', '2025-10-14', '09:03:00', 'Convention Center, New York', 'images/blockchain_meetup.jpg', 'networking', 25, 200, 200, 62, 50, 50, '2025-06-06 04:44:50', 1);
INSERT INTO `events` VALUES (83, 'Business Networking Lunch 2026', 'Don\'t miss this exclusive concert at City Conference Hall, Denver.', '2025-06-07', '07:37:00', 'City Conference Hall, Denver', 'images/tech_conference_2023.jpg', 'concert', 30, 1000, 1000, 60, 500, 500, '2025-06-06 04:44:50', 23);
INSERT INTO `events` VALUES (84, 'Digital Marketing Seminar 2026', 'Don\'t miss this exclusive concert at Science Center, Seattle.', '2025-12-17', '04:25:00', 'Science Center, Seattle', 'images/healthcare_innovation_forum.jpg', 'concert', 75, 100, 100, 150, 50, 50, '2025-06-06 04:44:50', 29);
INSERT INTO `events` VALUES (85, 'AI & ML Conference 2026', 'Connect and learn at our networking in Science Center, Seattle.', '2025-09-26', '05:59:00', 'Science Center, Seattle', 'images/tech_conference_2023.jpg', 'networking', 50, 50, 50, 75, 12, 12, '2025-06-06 04:44:50', 29);
INSERT INTO `events` VALUES (86, 'Summer Music Festival 2026', 'Don\'t miss this exclusive conference at Convention Center, New York.', '2025-10-15', '20:24:00', 'Convention Center, New York', 'images/web_development_workshop.jpg', 'conference', 40, 1000, 1000, 60, 200, 200, '2025-06-06 04:44:50', 24);
INSERT INTO `events` VALUES (87, 'Healthcare Innovation Forum 2026', 'Don\'t miss this exclusive conference at Downtown Arena, Los Angeles.', '2026-05-26', '20:15:00', 'Downtown Arena, Los Angeles', 'images/web_development_workshop.jpg', 'conference', 40, 1000, 1000, 100, 333, 333, '2025-06-06 04:44:50', 27);
INSERT INTO `events` VALUES (88, 'Summer Music Festival 2026', 'Don\'t miss this exclusive networking at Grand Hotel, Boston.', '2025-09-06', '19:26:00', 'Grand Hotel, Boston', 'images/film_media_expo.jpg', 'networking', 60, 100, 100, 90, 20, 20, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (89, 'Blockchain Meetup 2026', 'Join us for the biggest networking of the year in University Auditorium, Atlanta.', '2025-12-20', '16:54:00', 'University Auditorium, Atlanta', 'images/blockchain_meetup.jpg', 'networking', 75, 1000, 1000, 187, 333, 333, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (90, 'Blockchain Meetup 2026', 'Don\'t miss this exclusive concert at Downtown Arena, Los Angeles.', '2026-03-09', '10:07:00', 'Downtown Arena, Los Angeles', 'images/blockchain_meetup.jpg', 'concert', 40, 50, 50, 60, 25, 25, '2025-06-06 04:44:50', 22);
INSERT INTO `events` VALUES (91, 'Business Networking Lunch 2026', 'A must-attend workshop for professionals, hosted at City Conference Hall, Denver.', '2025-07-10', '19:36:00', 'City Conference Hall, Denver', 'images/summer_music_festival.jpg', 'workshop', 60, 300, 300, 120, 60, 60, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (92, 'Web Development Workshop 2027', 'A must-attend workshop for professionals, hosted at Riverside Pavilion, Miami.', '2026-01-07', '22:55:00', 'Riverside Pavilion, Miami', 'images/healthcare_innovation_forum.jpg', 'workshop', 75, 300, 300, 187, 75, 75, '2025-06-06 04:44:50', 26);
INSERT INTO `events` VALUES (93, 'Blockchain Meetup 2027', 'Experience the latest in concert held at Convention Center, New York.', '2026-06-03', '03:17:00', 'Convention Center, New York', 'images/tech_conference_2023.jpg', 'concert', 20, 200, 200, 30, 66, 66, '2025-06-06 04:44:50', 30);
INSERT INTO `events` VALUES (94, 'Business Networking Lunch 2027', 'Experience the latest in conference held at Riverside Pavilion, Miami.', '2025-09-04', '02:49:00', 'Riverside Pavilion, Miami', 'images/blockchain_meetup.jpg', 'conference', 20, 200, 200, 30, 40, 40, '2025-06-06 04:44:50', 24);
INSERT INTO `events` VALUES (95, 'Startup Pitch Competition 2027', 'An unforgettable conference experience, happening at Riverside Pavilion, Miami.', '2026-04-12', '08:50:00', 'Riverside Pavilion, Miami', 'images/blockchain_meetup.jpg', 'conference', 25, 1000, 1000, 37, 333, 333, '2025-06-06 04:44:50', 29);
INSERT INTO `events` VALUES (96, 'Healthcare Innovation Forum 2027', 'Don\'t miss this exclusive conference at City Conference Hall, Denver.', '2025-07-26', '17:49:00', 'City Conference Hall, Denver', 'images/blockchain_meetup.jpg', 'conference', 100, 50, 50, 250, 16, 16, '2025-06-06 04:44:50', 23);
INSERT INTO `events` VALUES (97, 'Digital Marketing Seminar 2027', 'Don\'t miss this exclusive concert at Innovation Center, Austin.', '2025-09-29', '23:06:00', 'Innovation Center, Austin', 'images/business_networking_lunch.jpg', 'concert', 30, 100, 100, 75, 25, 25, '2025-06-06 04:44:50', 24);
INSERT INTO `events` VALUES (98, 'Healthcare Innovation Forum 2027', 'A must-attend conference for professionals, hosted at Grand Hotel, Boston.', '2026-02-07', '11:44:00', 'Grand Hotel, Boston', 'images/startup_pitch_competition.jpg', 'conference', 60, 300, 300, 120, 75, 75, '2025-06-06 04:44:50', 2);
INSERT INTO `events` VALUES (99, 'Startup Pitch Competition 2027', 'A must-attend conference for professionals, hosted at Expo Hall, Chicago.', '2025-10-27', '21:02:00', 'Expo Hall, Chicago', 'images/film_media_expo.jpg', 'conference', 75, 50, 50, 150, 25, 25, '2025-06-06 04:44:50', 31);
INSERT INTO `events` VALUES (100, 'Healthcare Innovation Forum 2027', 'Don\'t miss this exclusive conference at Convention Plaza, Dallas.', '2026-06-06', '01:33:00', 'Convention Plaza, Dallas', 'images/summer_music_festival.jpg', 'conference', 60, 300, 300, 90, 100, 100, '2025-06-06 04:44:50', 25);
INSERT INTO `events` VALUES (101, 'Summer Music Festival 2027', 'A must-attend conference for professionals, hosted at Grand Hotel, Boston.', '2026-05-09', '14:53:00', 'Grand Hotel, Boston', 'images/startup_pitch_competition.jpg', 'conference', 40, 500, 500, 60, 100, 100, '2025-06-06 04:44:50', 20);
INSERT INTO `events` VALUES (102, 'Tech Conference 2028', 'An unforgettable workshop experience, happening at University Auditorium, Atlanta.', '2025-10-05', '05:17:00', 'University Auditorium, Atlanta', 'images/startup_pitch_competition.jpg', 'workshop', 25, 500, 500, 50, 100, 100, '2025-06-06 04:44:50', 20);

-- ----------------------------
-- Table structure for notifications
-- ----------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `read` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_notifications_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_notifications_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notifications
-- ----------------------------
INSERT INTO `notifications` VALUES (1, 7, 'Welcome to EventHub!', 'Thank you for joining EventHub. Start exploring events now!', '2023-05-01 00:00:00', 0);
INSERT INTO `notifications` VALUES (2, 2, 'Registration Confirmed for Summer Music Festival', 'You have successfully registered for Summer Music Festival.', '2025-06-04 07:28:15', 0);
INSERT INTO `notifications` VALUES (3, 2, 'Registration Confirmed', 'Your registration for Summer Music Festival has been confirmed. Check your tickets in the dashboard.', '2025-06-04 07:28:15', 0);
INSERT INTO `notifications` VALUES (4, 2, 'Registration Confirmed for Summer Music Festival', 'You have successfully registered for Summer Music Festival.', '2025-06-04 07:35:08', 0);
INSERT INTO `notifications` VALUES (5, 2, 'Registration Confirmed', 'Your registration for Summer Music Festival has been confirmed. Check your tickets in the dashboard.', '2025-06-04 07:35:08', 0);
INSERT INTO `notifications` VALUES (6, 7, 'Registration Confirmed for Web Development Workshop', 'You have successfully registered for Web Development Workshop.', '2025-06-04 08:14:22', 0);
INSERT INTO `notifications` VALUES (7, 7, 'Registration Confirmed', 'Your registration for Web Development Workshop has been confirmed. Check your tickets in the dashboard.', '2025-06-04 08:14:22', 0);
INSERT INTO `notifications` VALUES (8, 7, 'Registration Confirmed for Summer Music Festival', 'You have successfully registered for Summer Music Festival.', '2025-06-05 13:39:50', 0);
INSERT INTO `notifications` VALUES (9, 7, 'Registration Confirmed', 'Your registration for Summer Music Festival has been confirmed. Check your tickets in the dashboard.', '2025-06-05 13:39:50', 0);

-- ----------------------------
-- Table structure for registrations
-- ----------------------------
DROP TABLE IF EXISTS `registrations`;
CREATE TABLE `registrations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `event_id` int NOT NULL,
  `ticket_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `quantity` int NOT NULL DEFAULT 1,
  `total_price` double NOT NULL DEFAULT 0,
  `purchase_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `attendee_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `attendee_email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `attendee_phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_registrations_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_registrations_event_id`(`event_id` ASC) USING BTREE,
  CONSTRAINT `fk_registrations_event` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_registrations_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of registrations
-- ----------------------------
INSERT INTO `registrations` VALUES (1, 7, 2, 'general', 1, 75, '2025-06-04 07:28:15', 'admin', '1558002781@qq.com', '18260652209');
INSERT INTO `registrations` VALUES (2, 7, 2, 'general', 1, 75, '2025-06-04 07:35:08', '吕晨宁', '1558002781@qq.com', '18260652209');
INSERT INTO `registrations` VALUES (3, 7, 4, 'general', 1, 25, '2025-06-04 08:14:22', '吕晨宁', '1558002781@qq.com', '18260652209');
INSERT INTO `registrations` VALUES (4, 7, 2, 'general', 1, 75, '2025-06-05 13:39:50', '吕晨宁', '1558002781@qq.com', '18260652209');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'user',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `interests` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uniq_users_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'Tech Events Inc.', 'organizer@techevents.com', 'password123', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (2, 'Music Festivals LLC', 'info@musicfestivals.com', 'password123', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (3, 'Business Network Association', 'contact@bna.com', 'password123', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (4, 'Code Academy', 'workshops@codeacademy.com', 'password123', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (5, 'Startup Accelerator', 'events@startupaccelerator.com', 'password123', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (6, 'John Doe', 'john@example.com', 'password123', 'user', NULL, NULL, NULL, NULL, NULL, '2025-06-04 14:10:47');
INSERT INTO `users` VALUES (7, 'JJ', 'john.doe@demo.com', 'pbkdf2:sha256:1000000$7yB9wULK$da2e6987f9c6a25ff7d996fd1e05262eba145b92ffbe9c6a1d6be1c25cc0e3fd', 'user', '', '', '', '', '', '2025-06-04 07:52:16');
INSERT INTO `users` VALUES (20, 'Tech Events Inc.', 'tech@demo.com', 'pbkdf2:sha256:1000000$GgYvnktz$9e57940930ef18c4a63539972a6004d84d7a5a29a8aff3ef781272f206229436', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-06 04:34:27');
INSERT INTO `users` VALUES (21, 'Music Festivals LLC', 'music@demo.com', 'pbkdf2:sha256:1000000$vvjPBltC$5577671bcede0759e5e63c6b4339cf1d0ba2c7c5b2160db82245fe431808f95b', 'organizer', NULL, NULL, NULL, NULL, NULL, '2025-06-06 04:34:28');
INSERT INTO `users` VALUES (22, 'Organizer 1', 'organizer1@example.com', 'pbkdf2:sha256:1000000$JK54lNde$77b529ef6ebcef89a5a61fce7ef0e66cea6b714a67f7f6c1d07c86bc4d0a8479', 'organizer', '', '', '', '', '', '2025-06-06 04:44:47');
INSERT INTO `users` VALUES (23, 'Organizer 2', 'organizer2@example.com', 'pbkdf2:sha256:1000000$wT3QZfWt$947f053bf01437cdb36dcfcec67ef561665bbde54c1fb0cd2867420fabd9b931', 'organizer', '', '', '', '', '', '2025-06-06 04:44:47');
INSERT INTO `users` VALUES (24, 'Organizer 3', 'organizer3@example.com', 'pbkdf2:sha256:1000000$z1q8JPim$67e6fa84a6807b1ecd00f1cc1af8cccd0f30109936329d393b7dd625e520b2ba', 'organizer', '', '', '', '', '', '2025-06-06 04:44:47');
INSERT INTO `users` VALUES (25, 'Organizer 4', 'organizer4@example.com', 'pbkdf2:sha256:1000000$b4Joz6c0$30e8554f99548c3d18fc3430e232ad50f5cf0d287d1640e6d565796bcd9f312c', 'organizer', '', '', '', '', '', '2025-06-06 04:44:48');
INSERT INTO `users` VALUES (26, 'Organizer 5', 'organizer5@example.com', 'pbkdf2:sha256:1000000$1xPyqijY$1a4603c1876233ef0ca52913ca84ef2a32878b0ea608beba302d615ed5af7579', 'organizer', '', '', '', '', '', '2025-06-06 04:44:48');
INSERT INTO `users` VALUES (27, 'Organizer 6', 'organizer6@example.com', 'pbkdf2:sha256:1000000$P3pPSHI2$f48c8f9f37574ffb66b043bedd1d6e60fff7ce96c27e0e2fa4e1ea752cc8cb50', 'organizer', '', '', '', '', '', '2025-06-06 04:44:48');
INSERT INTO `users` VALUES (28, 'Organizer 7', 'organizer7@example.com', 'pbkdf2:sha256:1000000$28GCDJOA$0c06c1c13f8b041bf2e5cd712bb85e3348165e2856d6ceba02acd309c6990899', 'organizer', '', '', '', '', '', '2025-06-06 04:44:49');
INSERT INTO `users` VALUES (29, 'Organizer 8', 'organizer8@example.com', 'pbkdf2:sha256:1000000$VrT9KMLX$750741cd7aac93f02f1c930e0a93f3af20cf42e81642e5f7054afae6950bafde', 'organizer', '', '', '', '', '', '2025-06-06 04:44:49');
INSERT INTO `users` VALUES (30, 'Organizer 9', 'organizer9@example.com', 'pbkdf2:sha256:1000000$ElXr4xqy$2b033638f855059b19d17df2f1afe414a30e900d22aa80986263ae4f30e305be', 'organizer', '', '', '', '', '', '2025-06-06 04:44:50');
INSERT INTO `users` VALUES (31, 'Organizer 10', 'organizer10@example.com', 'pbkdf2:sha256:1000000$sqodKQ9n$ec064c19d86f1f4433eccf70928503623daec5ac648ee6a1161cc412235b3036', 'organizer', '', '', '', '', '', '2025-06-06 04:44:50');

SET FOREIGN_KEY_CHECKS = 1;
