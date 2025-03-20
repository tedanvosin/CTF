<?php
class Database
{
    public function __construct($file)
    {
        if (!file_exists($file))
        {
            file_put_contents($file, '');
        }
        $this->db = new SQLite3($file);
        $this->migrate();
    }

    public function migrate()
    {
        $this->db->query('
            CREATE TABLE IF NOT EXISTS `users` (
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        ');
    }

    public function register($username, $password)
    {
        $stmt = $this->db->prepare('INSERT INTO users (username, password) VALUES(?,?)');
        $stmt->bindValue(1, $username, SQLITE3_TEXT);
        $stmt->bindValue(2, $password, SQLITE3_TEXT);

        return $stmt->execute();
    }

    public function login($username, $password)
    {
        $stmt = $this->db->prepare('SELECT * FROM users WHERE username = ? AND password = ?');
        $stmt->bindValue(1, $username, SQLITE3_TEXT);
        $stmt->bindValue(2, $password, SQLITE3_TEXT);

        $result = $stmt->execute();
        return $result->fetchArray(SQLITE3_ASSOC)['username'];
    }
}