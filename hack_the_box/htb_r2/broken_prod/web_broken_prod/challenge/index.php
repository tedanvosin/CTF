<?php
spl_autoload_register(function ($name){
    if (preg_match('/Controller$/', $name))
    {
        $name = "controllers/${name}";
    }
    else if (preg_match('/Model$/', $name))
    {
        $name = "models/${name}";
    }
    include_once "${name}.php";
});

$session  = new SessionHandler();
$database = new Database('/tmp/challenge.db');

$router = new Router();
$router->new('GET', '/', function($router) use ($session){
    if (!$session->isLoggedIn()) 
    {
        return header('location: /login');
    }

    return $router->view('index', ['admin' => $session->isAdmin(), 'username' => $session->getUsername()]);
});

$router->new('GET', '/login', function($router)  use ($session){
    if ($session->isLoggedIn()) 
    {
        return header('location: /');
    }

    return $router->view('login');
});

$router->new('GET', '/register', function($router)  use ($session){
    if ($session->isLoggedIn()) 
    {
        return header('location: /');
    }

    return $router->view('register');
});

$router->new('POST', '/auth/login', function($router) use ($database, $session){
    $user = $database->login($_POST['username'], $_POST['password']);
    if (!$user) return header('location: /login?msg=Invalid username or password!');
    $session->login($_POST['username']);
    header('location: /');
    exit;
});

$router->new('POST', '/auth/register', function($router)  use ($database){
    if ($_POST['username'] === 'admin') return header('location: /register?msg=This user already exists!');
    $database->register($_POST['username'], $_POST['password']);
    header('location: /login?msg=The account registered successfully!&reg=true');
    exit;
});


$router->new('GET', '/logout', function($router)  use ($session){
    
    $session->distroy();
    return header('location: /login');
    
});


die($router->match());