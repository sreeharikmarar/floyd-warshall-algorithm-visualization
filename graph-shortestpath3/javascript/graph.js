if(window.addEventListener) {
window.addEventListener('load', function () {

var draw_path = [];
var adj_list = [];
var nodes = [];
var weight = [];
var i=1,n1,n2,j,k;
var v1,v2;
var count = 0;
nodes[0] = [0,0];
adj_list[0] = 0;
canvas.addEventListener("dblclick", handleDoubleClick, false); 
canvas.addEventListener("mouseup", handleMouseUp, false);
canvas.addEventListener("mousedown", handleMouseDown, false);

        $(document).ready(function(){

         $("#btn2").click(function(){
           var parameters = {"adj[]":adj_list, "nods[]":nodes, 'edge_wt[]':weight, "length": i};
           $.post(
               "/byweight",
               parameters,
               function(result){
		
               $("#text2").val(result);
               });
           });

	
         $("#btnw").click(function(){
	
	   var t1 = $("#tb1").val()
	   var t2 = $("#tb2").val()
           var parameters = {"adj[]":adj_list, "nods[]":nodes, 'edge_wt[]':weight, "length": i,'t1':t1 , 't2':t2};
           $.post(
               "/byweight_bx",
               parameters,
               function(result){
		
	
             $("#text2").val(result);
               });
           });



        
	$("#click").click(function(){
		

	   var t1 = $("#tb1").val()
	   var t2 = $("#tb2").val()
	
           var parameters = {"adj[]":adj_list, "nods[]":nodes, 'edge_wt[]':weight, "length": i,'t1':t1 , 't2':t2};
           $.post(
               "/draw",
               parameters,
               function(result){
		
		var str = result;
		var strarray = new Array();

		strarray = str.split(",");
		for (a in strarray) 
		{

		strarray[a] = parseInt(strarray[a]);
		}
		strarray[0] = t1;		
		var i;

		
		var c=document.getElementById("canvas");
	
    		var cxt1=c.getContext("2d");

		
    			for(i = 0;i <strarray.length;i=i+1)
			{
	                
	               		w1 = nodes[strarray[i]][0];
				w2 = nodes[strarray[i]][1];
				w3 = nodes[strarray[i+1]][0];
				w4 = nodes[strarray[i+1]][1];
		
				cxt1.beginPath();
				cxt1.moveTo(w1,w2); 
				cxt1.lineTo(w3,w4);
				cxt1.lineWidth = 5;
				cxt1.strokeStyle = "red";
	    			cxt1.stroke();
				
			
			}
		
		
               });
           });

	$("#refresh").click(function(){
		
	   var t1 = $("#tb1").val()
	   var t2 = $("#tb2").val()
	
           var parameters = {"adj[]":adj_list, "nods[]":nodes, 'edge_wt[]':weight, "length": i,'t1':t1 , 't2':t2};

           $.post(
		"/draw",
               parameters,
               function(result){
		
		var str = result;
		var strarray = new Array();

		strarray = str.split(",");
		for (a in strarray) 
		{

		strarray[a] = parseInt(strarray[a]);
		}
		strarray[0] = t1;		
		var i;

		
		var c=document.getElementById("canvas");
	
    		var cxt1=c.getContext("2d");

		
    			for(i = 0;i <strarray.length;i=i+1)
			{
	                
	               		w1 = nodes[strarray[i]][0];
				w2 = nodes[strarray[i]][1];
				w3 = nodes[strarray[i+1]][0];
				w4 = nodes[strarray[i+1]][1];
		
				cxt1.beginPath();
				cxt1.moveTo(w1,w2); 
				cxt1.lineTo(w3,w4);
				cxt1.lineWidth = 5;
				cxt1.strokeStyle = "black";
	    			cxt1.stroke();
				
			
			}
		
               });
           });
		
});


function handleDoubleClick(e)
{ 
        var msg = "";
    	var cell = getpos(e);
    	canvasX = cell.x-10;
    	canvasY = cell.y-10;
    	nodes[i]=[cell.x,cell.y];
		adj_list[i]=[];
    	var g_canvas = document.getElementById("canvas");
    	var context = g_canvas.getContext("2d");
	context.strokeStyle = "black";
    	var cat = new Image();
    	cat.src = "/images/dot.png";
        if (getpos != null) {
                msg =  cell.x +"," + cell.y;
        }
       
    	cat.onload = function() 
    	{
    	    context.drawImage(cat,canvasX , canvasY);
            
            context.fillText(i, canvasX+10, canvasY+30);
            i=i+1;
        }

}


function getpos(e) 
{
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;
    var x;
    var y;
    if (e.pageX != undefined && e.pageY != undefined) 
    {
        x = e.pageX;
        y = e.pageY;
    }
    else 
    {
        x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }
    x = x- canvas.offsetLeft;
    y = y- canvas.offsetTop;
    
    return {x:x, y:y}
}


var x1=0,x2=0,y1=0,y2=0;

function handleMouseDown(e)
{

    var c=document.getElementById("canvas");
    var cxt=c.getContext("2d");
    cxt.strokeStyle = "black";
    var cell = getpos(e);
    for(k=1;k<=nodes.length;k++)
    {
    	if(cell.x>=nodes[k][0]-10 && cell.x<=nodes[k][0]+10 && cell.y>=nodes[k][1]-10 && cell.y<=nodes[k][1]+10)
    	{
    	 	x1 = nodes[k][0];
    		y1 = nodes[k][1];
    		for(j=1;j<=nodes.length;j++)
    		{
    				if(x1==nodes[j][0] && y1==nodes[j][1]){
    					n1=j;
    				}
    		}
    
    	}
    	
    }

}


function handleMouseUp(e)
{
    var cell = getpos(e);
    for(k=1;k<=nodes.length;k++)
    {
    	if(cell.x>=nodes[k][0]-10 && cell.x<=nodes[k][0]+10 && cell.y>=nodes[k][1]-10 && cell.y<=nodes[k][1]+10)
    	{
    	 	x2 = nodes[k][0];
    		y2 = nodes[k][1];
    		var c=document.getElementById("canvas");
    		var cxt=c.getContext("2d");
    		cxt.strokeStyle = "black";
		cxt.moveTo(x1,y1);
    		cxt.lineTo(x2,y2);
		cxt.lineWidth = 5;
    		cxt.stroke(); 
		v1=x2-x1;
		v2=y2-y1;
		wt = Math.sqrt((v1*v1)+(v2*v2));
		wt = parseInt(wt);

 		for(j=1;j<=nodes.length;j++)
    		{
    				if(x2==nodes[j][0] && y2==nodes[j][1]){
    					n2=j;
    					adj_list[n1].push(n2);  					    		
					adj_list[n2].push(n1);
					weight.push(wt,n1,n2);

    				}
    		}   		
    	}
    	  	
    }

}

}, false); }
