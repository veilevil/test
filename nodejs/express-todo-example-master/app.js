/**
 * Module dependencies.
 */

var express = require("express")
    , http = require('http')
    , path = require('path');
var app = express();

// mongoose setup
require( './db' );

var routes = require( './routes' );

// Configuration
app.configure( 'development', function (){
    app.set('port', process.env.PORT || 3001);
  app.set( 'views', __dirname + '/views' );
  app.set( 'view engine', 'jade' );
  app.use( express.favicon());
  app.use( express.static( __dirname + '/public' ));
  app.use( express.logger());
  app.use( express.cookieParser());
  app.use( express.bodyParser());
  app.use( routes.current_user );
  app.use( app.router );
  app.use( express.errorHandler({ dumpExceptions : true, showStack : true }));
});

app.configure( 'production', function (){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use( express.cookieParser());
  app.use( express.bodyParser());
  app.use( routes.current_user );
  app.use( app.router );
  app.use( express.errorHandler());
});

// Routes
app.get( '/', routes.index );
app.get( '/todos', routes.getall );
app.put( '/create', routes.create );
app.post( '/edit', routes.edit );
app.delete( '/destroy/:id', routes.destroy );
app.get( '/edit/:id', routes.edit );
//app.post( '/update/:id', routes.update );
app.post( '/update', routes.update );

http.createServer(app).listen(app.get('port'), function(){
    console.log('Express server listening on port %d in %s mode', app.get('port'), app.get('env'));
});
