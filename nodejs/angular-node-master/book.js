var bookList=[
{
	id:1,
	title:'javascript',
	author:'Hass',
},
{
	id:2,
	title:'nodejs',
	author:'James',
},
{
	id:3,
	title:'mongodb',
	author:'Mike',
},
{
	id:4,
	title:'mysql',
	author:'John',
}];

exports.findAll=function(req,res){
	res.send(bookList);
}

exports.add=function(req,res){
	var book=req.body;
	book.id=bookList.length+1;
	bookList.push(book);
	res.send(book);
}

