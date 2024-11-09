CREATE TABLE channels (
                          id BIGINT NOT NULL,
                          name TEXT DEFAULT NULL,
                          type TEXT DEFAULT NULL,
                          topic TEXT DEFAULT NULL,
                          last_message_id TEXT DEFAULT NULL,
                          nsfw BOOLEAN DEFAULT FALSE,
                          PRIMARY KEY (id)
);

CREATE TABLE users (
                       id BIGINT NOT NULL,
                       username TEXT DEFAULT NULL,
                       global_name TEXT DEFAULT NULL,
                       avatar TEXT DEFAULT NULL,
                       avatar_url TEXT DEFAULT NULL,
                       discriminator TEXT DEFAULT NULL,
                       flags INT DEFAULT NULL,
                       accent_color TEXT DEFAULT NULL,
                       banner TEXT DEFAULT NULL,
                       banner_color TEXT DEFAULT NULL,
                       bot BOOLEAN DEFAULT NULL,
                       bio TEXT DEFAULT NULL,
                       pronouns TEXT DEFAULT NULL,
                       public_flags INT DEFAULT NULL,
                       mutual_friends_count INT DEFAULT NULL,
                       PRIMARY KEY (id)
);

CREATE TABLE guilds (
                        id BIGINT NOT NULL,
                        name TEXT DEFAULT NULL,
                        icon TEXT DEFAULT NULL,
                        owner BIGINT DEFAULT NULL,
                        region TEXT DEFAULT NULL,
                        member_count INT DEFAULT NULL,
                        verification_level TEXT DEFAULT NULL,
                        permissions TEXT DEFAULT NULL,
                        features TEXT DEFAULT NULL,
                        PRIMARY KEY (id)
);
CREATE TABLE messages (
                          id BIGINT NOT NULL,
                          content TEXT DEFAULT NULL,
                          channel_id BIGINT DEFAULT NULL,
                          guild_id BIGINT DEFAULT NULL,
                          user_id BIGINT DEFAULT NULL,
                          timestamp BIGINT DEFAULT NULL,
                          embeds JSON DEFAULT NULL,
                          components JSON DEFAULT NULL,
                          attachments JSON DEFAULT NULL,
                          mentions JSON DEFAULT NULL,
                          reference TEXT DEFAULT NULL,
                          PRIMARY KEY (id)
);

CREATE TABLE mutual_guilds (
                               user_id BIGINT NOT NULL,
                               guild_id BIGINT NOT NULL,
                               nick TEXT DEFAULT NULL,
                               PRIMARY KEY (user_id, guild_id),
                               FOREIGN KEY (user_id) REFERENCES users(id),
                               FOREIGN KEY (guild_id) REFERENCES guilds(id)
);

/* Primary key rationale:
   - Composite primary key on `user_id` and `guild_id` to ensure each mutual guild association is unique per user.
   - `nic` column allows for additional information related to the mutual guild.
*/

CREATE TABLE mutual_friends (
                                user_id BIGINT NOT NULL,
                                friend_id BIGINT NOT NULL,
                                PRIMARY KEY (user_id, friend_id),
                                FOREIGN KEY (user_id) REFERENCES users(id),
                                FOREIGN KEY (friend_id) REFERENCES users(id)
);

/* Primary key rationale:
   - Composite primary key on `user_id` and `friend_id` to ensure each mutual friend relationship is unique.
   - Both `user_id` and `friend_id` reference the `users` table, establishing the mutual friendship.
*/