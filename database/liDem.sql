-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 20. Jul 2019 um 18:29
-- Server-Version: 5.7.26-0ubuntu0.18.10.1
-- PHP-Version: 7.2.19-0ubuntu0.18.10.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `liDem`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Club`
--

CREATE TABLE `Club` (
  `ID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Motto` varchar(100) NOT NULL,
  `Description` text NOT NULL,
  `Icon` varchar(100) NOT NULL,
  `PollCreatorLevel` int(11) NOT NULL DEFAULT '1',
  `InvitationKey` tinytext CHARACTER SET latin1 COLLATE latin1_general_cs,
  `AuthorID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Comment`
--

CREATE TABLE `Comment` (
  `ID` int(11) NOT NULL,
  `ClubID` int(11) NOT NULL,
  `Content` text NOT NULL,
  `AuthorID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `CommentComment`
--

CREATE TABLE `CommentComment` (
  `CommentID` int(11) NOT NULL,
  `CommentedID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `CommentProposal`
--

CREATE TABLE `CommentProposal` (
  `CommentID` int(11) NOT NULL,
  `ProposalID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `CommentTender`
--

CREATE TABLE `CommentTender` (
  `CommentID` int(11) NOT NULL,
  `TenderID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `CommentUser`
--

CREATE TABLE `CommentUser` (
  `CommentID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Evaluation`
--

CREATE TABLE `Evaluation` (
  `ID` int(11) NOT NULL,
  `TenderID` int(11) NOT NULL,
  `AuthorID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Follow`
--

CREATE TABLE `Follow` (
  `ID` int(11) NOT NULL,
  `FollowerID` int(11) NOT NULL,
  `FollowedID` int(11) NOT NULL,
  `ClubID` int(11) NOT NULL,
  `Weight` double NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Log`
--

CREATE TABLE `Log` (
  `ID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Content` text NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Member`
--

CREATE TABLE `Member` (
  `UserID` int(11) NOT NULL,
  `ClubID` int(11) NOT NULL,
  `Level` int(11) NOT NULL,
  `GranterID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Proposal`
--

CREATE TABLE `Proposal` (
  `ID` int(11) NOT NULL,
  `TenderID` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Description` text NOT NULL,
  `Icon` varchar(100) NOT NULL,
  `AuthorID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Result`
--

CREATE TABLE `Result` (
  `ID` int(11) NOT NULL,
  `EvaluationID` int(11) NOT NULL,
  `ProposalID` int(11) NOT NULL,
  `Outcome` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ResultDetail`
--

CREATE TABLE `ResultDetail` (
  `ResultID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Weight` double NOT NULL,
  `Value` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Tender`
--

CREATE TABLE `Tender` (
  `ID` int(11) NOT NULL,
  `ClubID` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Description` text NOT NULL,
  `Secret` tinyint(1) NOT NULL,
  `Phase` int(11) NOT NULL,
  `Icon` varchar(100) NOT NULL,
  `ChoiceCreatorLevel` int(11) NOT NULL DEFAULT '1',
  `AuthorID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `EndPhase0` timestamp NULL DEFAULT NULL,
  `EndPhase1` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `User`
--

CREATE TABLE `User` (
  `ID` int(11) NOT NULL,
  `Username` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Password` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `Description` text NOT NULL,
  `Icon` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `ResetKey` tinytext CHARACTER SET latin1 COLLATE latin1_general_cs,
  `ResetTimestamp` timestamp NULL DEFAULT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Vote`
--

CREATE TABLE `Vote` (
  `ID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `ProposalID` int(11) NOT NULL,
  `Value` double NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Club`
--
ALTER TABLE `Club`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Indizes für die Tabelle `Comment`
--
ALTER TABLE `Comment`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `AuthorID` (`AuthorID`);

--
-- Indizes für die Tabelle `CommentComment`
--
ALTER TABLE `CommentComment`
  ADD KEY `CommentID` (`CommentID`),
  ADD KEY `CommentedID` (`CommentedID`);

--
-- Indizes für die Tabelle `CommentProposal`
--
ALTER TABLE `CommentProposal`
  ADD KEY `CommentID` (`CommentID`),
  ADD KEY `ProposalID` (`ProposalID`);

--
-- Indizes für die Tabelle `CommentTender`
--
ALTER TABLE `CommentTender`
  ADD KEY `CommentID` (`CommentID`),
  ADD KEY `TenderID` (`TenderID`);

--
-- Indizes für die Tabelle `CommentUser`
--
ALTER TABLE `CommentUser`
  ADD KEY `CommentID` (`CommentID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indizes für die Tabelle `Evaluation`
--
ALTER TABLE `Evaluation`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `TenderID` (`TenderID`);

--
-- Indizes für die Tabelle `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `FollowerID` (`FollowerID`),
  ADD KEY `FollowedID` (`FollowedID`),
  ADD KEY `ClubID` (`ClubID`);

--
-- Indizes für die Tabelle `Log`
--
ALTER TABLE `Log`
  ADD PRIMARY KEY (`ID`);

--
-- Indizes für die Tabelle `Member`
--
ALTER TABLE `Member`
  ADD KEY `Member_ibfk_1` (`UserID`),
  ADD KEY `Member_ibfk_2` (`ClubID`);

--
-- Indizes für die Tabelle `Proposal`
--
ALTER TABLE `Proposal`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `TenderID` (`TenderID`),
  ADD KEY `AuthorID` (`AuthorID`);

--
-- Indizes für die Tabelle `Result`
--
ALTER TABLE `Result`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `EvaluationID` (`EvaluationID`),
  ADD KEY `ProposalID` (`ProposalID`);

--
-- Indizes für die Tabelle `ResultDetail`
--
ALTER TABLE `ResultDetail`
  ADD KEY `ResultID` (`ResultID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indizes für die Tabelle `Tender`
--
ALTER TABLE `Tender`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `ClubID` (`ClubID`),
  ADD KEY `AuthorID` (`AuthorID`);

--
-- Indizes für die Tabelle `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD KEY `ID_2` (`ID`);

--
-- Indizes für die Tabelle `Vote`
--
ALTER TABLE `Vote`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ProposalID` (`ProposalID`),
  ADD KEY `UserID` (`UserID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Club`
--
ALTER TABLE `Club`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- AUTO_INCREMENT für Tabelle `Comment`
--
ALTER TABLE `Comment`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;
--
-- AUTO_INCREMENT für Tabelle `Evaluation`
--
ALTER TABLE `Evaluation`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=185;
--
-- AUTO_INCREMENT für Tabelle `Follow`
--
ALTER TABLE `Follow`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;
--
-- AUTO_INCREMENT für Tabelle `Log`
--
ALTER TABLE `Log`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=365;
--
-- AUTO_INCREMENT für Tabelle `Proposal`
--
ALTER TABLE `Proposal`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;
--
-- AUTO_INCREMENT für Tabelle `Result`
--
ALTER TABLE `Result`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=478;
--
-- AUTO_INCREMENT für Tabelle `Tender`
--
ALTER TABLE `Tender`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;
--
-- AUTO_INCREMENT für Tabelle `User`
--
ALTER TABLE `User`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT für Tabelle `Vote`
--
ALTER TABLE `Vote`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=222;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Comment`
--
ALTER TABLE `Comment`
  ADD CONSTRAINT `Comment_ibfk_1` FOREIGN KEY (`AuthorID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `CommentComment`
--
ALTER TABLE `CommentComment`
  ADD CONSTRAINT `CommentComment_ibfk_1` FOREIGN KEY (`CommentID`) REFERENCES `Comment` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `CommentComment_ibfk_2` FOREIGN KEY (`CommentedID`) REFERENCES `Comment` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `CommentProposal`
--
ALTER TABLE `CommentProposal`
  ADD CONSTRAINT `CommentProposal_ibfk_1` FOREIGN KEY (`CommentID`) REFERENCES `Comment` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `CommentProposal_ibfk_2` FOREIGN KEY (`ProposalID`) REFERENCES `Proposal` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `CommentTender`
--
ALTER TABLE `CommentTender`
  ADD CONSTRAINT `CommentTender_ibfk_1` FOREIGN KEY (`CommentID`) REFERENCES `Comment` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `CommentTender_ibfk_2` FOREIGN KEY (`TenderID`) REFERENCES `Tender` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `CommentUser`
--
ALTER TABLE `CommentUser`
  ADD CONSTRAINT `CommentUser_ibfk_1` FOREIGN KEY (`CommentID`) REFERENCES `Comment` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `CommentUser_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Evaluation`
--
ALTER TABLE `Evaluation`
  ADD CONSTRAINT `Evaluation_ibfk_1` FOREIGN KEY (`TenderID`) REFERENCES `Tender` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `Follow_ibfk_1` FOREIGN KEY (`FollowerID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Follow_ibfk_2` FOREIGN KEY (`FollowedID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Follow_ibfk_3` FOREIGN KEY (`ClubID`) REFERENCES `Club` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Member`
--
ALTER TABLE `Member`
  ADD CONSTRAINT `Member_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Member_ibfk_2` FOREIGN KEY (`ClubID`) REFERENCES `Club` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Proposal`
--
ALTER TABLE `Proposal`
  ADD CONSTRAINT `Proposal_ibfk_1` FOREIGN KEY (`TenderID`) REFERENCES `Tender` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Proposal_ibfk_2` FOREIGN KEY (`AuthorID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Result`
--
ALTER TABLE `Result`
  ADD CONSTRAINT `Result_ibfk_1` FOREIGN KEY (`EvaluationID`) REFERENCES `Evaluation` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Result_ibfk_2` FOREIGN KEY (`ProposalID`) REFERENCES `Proposal` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `ResultDetail`
--
ALTER TABLE `ResultDetail`
  ADD CONSTRAINT `ResultDetail_ibfk_1` FOREIGN KEY (`ResultID`) REFERENCES `Result` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ResultDetail_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Tender`
--
ALTER TABLE `Tender`
  ADD CONSTRAINT `Tender_ibfk_1` FOREIGN KEY (`ClubID`) REFERENCES `Club` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Tender_ibfk_2` FOREIGN KEY (`AuthorID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `Vote`
--
ALTER TABLE `Vote`
  ADD CONSTRAINT `Vote_ibfk_2` FOREIGN KEY (`ProposalID`) REFERENCES `Proposal` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Vote_ibfk_3` FOREIGN KEY (`UserID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
