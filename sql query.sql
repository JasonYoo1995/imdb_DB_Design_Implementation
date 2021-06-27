use assignment;
show tables;

select * from Movie;
select count(*) from Movie;
# truncate Movie;
create table Movie(
	tconst varchar(10) primary key,
    titleType varchar(50),
    primaryTitle varchar(100),
    originalTitle varchar(100),
    isAdult varchar(1),
	startYear int,
    endYear int,
    runtimeMinutes int
);

select * from Rating;
select count(*) from Rating;
#truncate Rating;
create table Rating(
	tconst varchar(10) primary key,
    averageRating float,
    numVotes int,
    foreign key (tconst) references Movie(tconst)
);

select * from Genre;
select count(*) from Genre;
#truncate Genre;
create table Genre(
	sequence int auto_increment,
    tconst varchar(10),
    genre varchar(20),
    primary key (sequence, tconst),
    foreign key (tconst) references Movie(tconst)
);

select * from Director;
select count(*) from Director;
#truncate Director;
create table Director(
	sequence int auto_increment,
    tconst varchar(10),
    director varchar(20),
    primary key (sequence, tconst),
    foreign key (tconst) references Movie(tconst)
);

select * from Writer;
select count(*) from Writer;
#truncate Writer;
create table Writer(
	sequence int auto_increment,
    tconst varchar(10),
    writer varchar(20),
    primary key (sequence, tconst),
    foreign key (tconst) references Movie(tconst)
);

select * from Episode;
select count(*) from Episode;
#truncate Episode;
create table Episode(
	childTconst varchar(10),
    parentTconst varchar(10),
    seasonNumber int,
    episodeNumber int,
    primary key (childTconst, parentTconst),
    foreign key (childTconst) references Movie(tconst),
    foreign key (parentTconst) references Movie(tconst)
);

select * from Title;
select count(*) from Title;
#truncate Title;
create table Title(
	tconst varchar(10),
    ordering int,
	title varchar(100),
    region varchar(4),
	`language` varchar(4),
    isOriginalTitle varchar(1),
    primary key (tconst, ordering)
);

select * from `Type`;
select count(*) from `Type`;
#truncate `Type`;
create table `Type`(
	sequence int auto_increment,
    tconst varchar(10),
	ordering int,
    `type` varchar(20),
    primary key (sequence, tconst, ordering),
    foreign key (tconst, ordering) references Title(tconst, ordering)
);

select * from `Attribute`;
select count(*) from `Attribute`;
#truncate `Attribute`;
create table `Attribute`(
	sequence int auto_increment,
    tconst varchar(10),
	ordering int,
    `attribute` varchar(20),
    primary key (sequence, tconst, ordering),
    foreign key (tconst, ordering) references Title(tconst, ordering)
);

select * from `Name`;
select count(*) from `Name`;
#truncate `Name`;
create table `Name`(
	nconst varchar(12) primary key,
    primaryName varchar(50),
	birthYear int,
	deathYear int
);

select * from Profession;
select count(*) from Profession;
#truncate Profession;
create table Profession(
	sequence int auto_increment,
    nconst varchar(12),
    primaryProfession varchar(20),
    primary key (sequence, nconst),
    foreign key (nconst) references `Name`(nconst)
);

select * from RelatedMovie;
select count(*) from RelatedMovie;
#truncate RelatedMovie;
drop table RelatedMovie;
create table RelatedMovie(
	sequence int auto_increment,
    nconst varchar(12),
    tconst varchar(20),
    primary key (sequence, nconst),
    foreign key (nconst) references `Name`(nconst)	
);

select * from Principal;
select count(*) from Principal;
#truncate Principal;
drop table Principal;
create table Principal(
	tconst varchar(10),
    ordering int,
    nconst varchar(12),
    category varchar(20),
    job varchar(20),
    characters varchar(40),
    primary key (tconst, ordering),
    foreign key (tconst) references Movie(tconst)
);








 

### 영화제목을 입력하여, 이에 매칭되는 영화를 검색 ###
select * from Movie;
select count(*) from Movie;
select * from Movie where primaryTitle="Miss Jerry";
select * from Movie where tconst="tt1999999";
# 인덱싱
show index from Movie;
alter table Movie add index primaryTitle_idx(primaryTitle);
#alter table Movie drop index primaryTitle_idx;

### 특정 배우가 등장하는 영화를 별점이 높은 순으로 검색 ###
select n.primaryName, m.originalTitle, r.averageRating from
(Rating r join Movie m on r.tconst = m.tconst) join (RelatedMovie rm join `Name` n on rm.nconst = n.nconst) on rm.tconst = r.tconst
where n.primaryName="Richard Burton"
order by r.averageRating desc;
# 인덱싱
show index from RelatedMovie;
alter table RelatedMovie add index nconst_idx(nconst);
#alter table RelatedMovie drop index nconst_idx;

### 특정 감독이 제작한 영화를 개봉연도순으로 검색 ###
select n.primaryName, m.originalTitle, m.startYear
from Movie m join Principal p on m.tconst = p.tconst join `Name` n on p.nconst = n.nconst
where n.primaryName='William K.L. Dickson'
order by m.startYear;
# 인덱싱
show index from Principal;
alter table Principal add index nconst_idx(nconst);
#alter table Principal drop index nconst_idx;

### Drama 장르의 영화를 리뷰가 많은 순으로 검색 ###
select g.genre, m.primaryTitle, r.numVotes
from Movie m join Genre g on m.tconst = g.tconst join Rating r on m.tconst = r.tconst
where g.genre = 'Drama'
order by r.numVotes desc;
# 인덱싱
show index from Rating;
alter table Rating add index numVotes_idx(numVotes);
#alter table Rating drop index numVotes_idx;

### Drama 장르의 영화를 별점이 높은순으로 검색 ###
select g.genre, m.primaryTitle, r.averageRating
from Movie m join Genre g on m.tconst = g.tconst join Rating r on m.tconst = r.tconst
where g.genre = "Drama"
order by r.averageRating desc
limit 10;
# 인덱싱
show index from Rating;
alter table Rating add index averageRating_idx(averageRating);
#alter table Rating drop index averageRating_idx;

### group by를 사용하는 query : 영화별 상영 지역 개수 검색 ###
select m.originalTitle, count(t.region)
from Title t join Movie m on t.tconst = m.tconst
group by m.tconst;








use mysql;
select * from user;
grant all privileges on assignment.* to `db2020`@`%`;
update user set `authentication_string`=PASSWORD('********') where user='root';
alter user 'root'@'localhost' identified with mysql_native_password by '********';
flush privileges;

set global sql_mode="";
SET @@global.sql_mode= 'NO_ENGINE_SUBSTITUTION';