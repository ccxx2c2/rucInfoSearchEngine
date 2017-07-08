//supervisor --harmony index
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var iconv = require("iconv-lite");
var fs = require('fs');
var exec = require('child_process').exec;


app.use(express.static(__dirname+'/public'));
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true }));

fs.readFile('public/index.html',function(err,data){
	if(err){
		console.log(err);
	}else{
		index = data.toString();
	}
});
console.log(__dirname);
app.get('/',function(req,res){
	res.send(index);
});
var child = exec('python query.py', function (err, stdout, stderr) {
  console.log(stdout);   // 直接查看输出
  console.log(stderr);   // 直接查看输出
});        
app.post('/reader',function(req,res){
      console.log(req.body.query);
      child.stdin.write(req.body.query+'\n');//child.stdin.write(iconv.encode(req.body.query+'\n','utf-8'));   // 输入
      child.stdout.once('data', function (s) {
            a=s.toString();
            console.log(a);//iconv.decode(a, 'gb2312')
            if(a[a.length-3]=="!"){
                console.log(a);
                res.send(JSON.parse("[]"));
                return;
            }
            var t=0;
            while(a[t]!='[') t+=1;
            a='['+a.substring(t,a.length-1)+']';
            res.send(JSON.parse(a));
      });
});

/*req.query.name: http://127.0.0.1:3000/?name=1*/
app.get('/users/:name',function(req,res){
	res.send('hello, '+req.params.name);
});
/*http://127.0.0.1:3000/users/123*/
app.listen(80);


