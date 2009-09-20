begin transaction;
set constraints all deferred;

create table tweet (
   id                   serial not null primary key,
   is_favorited         boolean,
   follower_count       int,
   friend_count         int,
   in_reply_screen_name text,
   in_reply_status_id   int,
   in_reply_user_id     int,
   screen_name          text,
   src                  text,
   status_count         int,
   tweet_id             int,
   username             text,
   tweet                text
);

commit;
