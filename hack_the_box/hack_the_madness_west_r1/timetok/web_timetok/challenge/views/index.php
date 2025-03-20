<html>
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
  <title>TimeTok</title>
  <link link='preload' href='//fonts.googleapis.com/css2?family=Press+Start+2P&display=swap' rel='stylesheet'>
  <link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>
  <link rel='stylesheet' href='/static/css/main.css' />
  <link rel='icon' href='/assets/favicon.png' />
</head>
<body>
<div id='main' class='container'>
  <h1 id='title'>🍒 TimeTok 🍒</h1>
  <br>
  <div id='img-div'>
    <img id='image' src='/assets/cyberpunk.gif' alt='eating space shrimps'>
    <br>
  </div>
  <hr>
  <h1 id='title'><span class='text-muted'>It's</span> <?= $time ?><span class='text-muted'>.</span></h1>
  <div class='form-group'>
    <div class='row'>
      <div class='col'>
        <a href='?format=%H:%M:%S' class='btn btn-danger btn-block'>What about now?</a>
      </div>
      <div class='col'>
          <a href='?format=%Y-%m-%d' class='btn btn-danger btn-block'>What's the date?</a>
      </div>
    </div>
  </div>
</div>
</body>
</html>