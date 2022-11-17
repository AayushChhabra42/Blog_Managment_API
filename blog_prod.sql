-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2022 at 09:00 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blog_prod`
--

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `Name` varchar(200) NOT NULL,
  `ID` int(6) NOT NULL,
  `Region` varchar(6) NOT NULL,
  `Created_at` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`Name`, `ID`, `Region`, `Created_at`) VALUES
('GRP1', 200000, 'ASIA', '2022-11-09'),
('GRP2', 200001, 'ASIA', '2022-11-09');

-- --------------------------------------------------------

--
-- Table structure for table `group_participants`
--

CREATE TABLE `group_participants` (
  `Group_ID` int(6) NOT NULL,
  `Participant_ID` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `group_participants`
--

INSERT INTO `group_participants` (`Group_ID`, `Participant_ID`) VALUES
(200000, 100000);

-- --------------------------------------------------------

--
-- Table structure for table `group_posts`
--

CREATE TABLE `group_posts` (
  `Group_ID` int(6) NOT NULL,
  `Post_ID` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `group_posts`
--

INSERT INTO `group_posts` (`Group_ID`, `Post_ID`) VALUES
(200000, 300000);

--
-- Triggers `group_posts`
--
DELIMITER $$
CREATE TRIGGER `group_participants_auto_ins` AFTER INSERT ON `group_posts` FOR EACH ROW BEGIN DECLARE test int(6);SELECT posts.creator_id into test from posts,group_posts where posts.ID=new.post_id limit 1; insert into group_participants(Group_ID,Participant_ID) VALUES(new.group_id,test); END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `Title` varchar(300) NOT NULL,
  `ID` int(6) NOT NULL,
  `Text` text NOT NULL,
  `Creator_ID` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`Title`, `ID`, `Text`, `Creator_ID`) VALUES
('This is the first post', 300000, 'this is content contained by the first post', 100000);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `Username` varchar(50) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(16) NOT NULL,
  `Joined_at` date NOT NULL DEFAULT current_timestamp(),
  `ID` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`Username`, `Email`, `Password`, `Joined_at`, `ID`) VALUES
('Aayush', 'tt@test.com', 'Pass123', '2022-11-09', 100000),
('Chaitanya01', 'te2@test.com', '123456789', '2022-11-09', 100001),
('test3', 'tets3@testnet.in', 'passs', '2022-11-11', 100002);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `group_participants`
--
ALTER TABLE `group_participants`
  ADD PRIMARY KEY (`Group_ID`,`Participant_ID`),
  ADD KEY `Participant_ID` (`Participant_ID`);

--
-- Indexes for table `group_posts`
--
ALTER TABLE `group_posts`
  ADD PRIMARY KEY (`Group_ID`,`Post_ID`),
  ADD KEY `Post_ID` (`Post_ID`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Creator_ID` (`Creator_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200002;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=300001;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100003;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `group_participants`
--
ALTER TABLE `group_participants`
  ADD CONSTRAINT `group_participants_ibfk_1` FOREIGN KEY (`Group_ID`) REFERENCES `groups` (`ID`),
  ADD CONSTRAINT `group_participants_ibfk_2` FOREIGN KEY (`Participant_ID`) REFERENCES `user` (`ID`);

--
-- Constraints for table `group_posts`
--
ALTER TABLE `group_posts`
  ADD CONSTRAINT `group_posts_ibfk_1` FOREIGN KEY (`Group_ID`) REFERENCES `groups` (`ID`),
  ADD CONSTRAINT `group_posts_ibfk_2` FOREIGN KEY (`Post_ID`) REFERENCES `posts` (`ID`);

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`Creator_ID`) REFERENCES `user` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
