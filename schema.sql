CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  discriminator TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic_url TEXT NOT NULL,
);
