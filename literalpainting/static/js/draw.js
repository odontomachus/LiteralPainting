lp = {}

lp.c = document.getElementById('canvas');
lp.ctx= lp.c.getContext("2d");

lp.line = function (x1,y1,x2,y2) {
    lp.ctx.moveTo(x1,y1);
    lp.ctx.lineTo(x2,y2);
    lp.ctx.stroke();
}

lp.circle = function (x1,y1,r) {
    lp.ctx.moveTo(x1+r,y1);
    lp.ctx.arc(x1,y1,r,0,2*Math.PI);
    lp.ctx.stroke();
}

lp.rectangle = function (x1,y1,x2,y2) {
    lp.ctx.moveTo(x1,y1);
    lp.ctx.rect(x1,y1,x2-x1,y2-y1);
    lp.ctx.stroke();
}

