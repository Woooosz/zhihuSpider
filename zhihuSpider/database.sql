-- phpMyAdmin SQL Dump
-- version 4.7.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 17, 2017 at 09:21 PM
-- Server version: 5.6.35
-- PHP Version: 7.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `zhihu`
--

-- --------------------------------------------------------

--
-- Table structure for table `person_info`
--

CREATE TABLE `person_info` (
  `name` varchar(10) NOT NULL,
  `gender` int(11) NOT NULL,
  `url_token` varchar(20) NOT NULL,
  `answer_count` int(11) NOT NULL,
  `voteup_count` int(11) NOT NULL,
  `thanked_count` int(11) NOT NULL,
  `participated_live_count` int(11) NOT NULL,
  `favorited_count` int(11) NOT NULL,
  `follower_count` int(11) NOT NULL,
  `following_count` int(11) NOT NULL,
  `locations` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
