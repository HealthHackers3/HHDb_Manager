-- noinspection SqlNoDataSourceInspectionForFile

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    poster_id INT NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(1000),
    category_id INT NOT NULL,
    cell_type_id INT NOT NULL,
    image_modality_id INT NOT NULL,
    cell_shape_id INT NOT NULL,
    likes INT DEFAULT 0 CHECK (likes >= 0),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (poster_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ,
    FOREIGN KEY (cell_type_id) REFERENCES cell_types(cell_type_id),
    FOREIGN KEY (cell_shape_id) REFERENCES cell_shapes(cell_shape_id)
)
--Types of image tag
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
)

CREATE TABLE cell_types (
    cell_type_id SERIAL PRIMARY KEY,
    cell_type_name VARCHAR(255) NOT NULL UNIQUE
)

CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(255) NOT NULL UNIQUE
)

CREATE TABLE cell_shapes (
    cell_shape_id SERIAL PRIMARY KEY,
    cell_shape_name VARCHAR(255) NOT NULL UNIQUE
)

CREATE TABLE image_modalities (
    image_modality_id SERIAL PRIMARY KEY,
    image_modality_name VARCHAR(255) NOT NULL UNIQUE
)

-- comment management
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    parent_comment_id INT DEFAULT NULL,
    comment_text TEXT NOT NULL,
    likes INT DEFAULT 0 CHECK (likes >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id)
);

CREATE TABLE comment_likes (
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    PRIMARY KEY (user_id, comment_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
);

-- image management
CREATE TABLE post_images (
    image_id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    order_index INT NOT NULL,
    image_file_name TEXT NOT NULL,
    cell_count INT DEFAULT 0 CHECK (cell_count >= 0),
    cell_dimensions_y INT DEFAULT 0 CHECK (cell_dimensions_y >= 0),
    cell_dimensions_x INT DEFAULT 0 CHECK (cell_dimensions_x >= 0),
    cell_density INT DEFAULT 0 CHECK (cell_density >= 0),
    image_path TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
)

CREATE TABLE post_likes (
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    UNIQUE (user_id, post_id),
    PRIMARY KEY(user_id, post_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)

CREATE TABLE user_profile_pics (
    user_id INT PRIMARY KEY,
    profile_pic BYTEA NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)

CREATE TABLE post_tags (
    post_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
)
