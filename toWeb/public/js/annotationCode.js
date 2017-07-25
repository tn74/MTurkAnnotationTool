

var CANVAS_WIDTH  = 420; // Need to change here and in the html document if desired
var CANVAS_HEIGHT = 420;

//global variables for the page
var img;
var canvas_fix;
var ctx;
var image_name; 
var category_name;
var table;
var ANNTYPE;
var base_url = ".";
var workingObj;
var IMG_COUNT = 0;
var RESULT_STRING = "";

var fullFile = function(fn) {
  this.annotations = new Array();
  this.fileName = fn;
  this.objs = new Array();
}

var polyObj = function(name, type) {
  this.name = name;
  this.type = type;
  this.data = [new Array(), new Array()];

  this.draw = function() {
    thisx = this.data[0];
    thisy = this.data[1];
    tp = thisx.length;
    for(i = 0; i < tp; i++) {
      plotx = thisx[i];
      ploty = thisy[i];
      for (j = 0; j< plotx.length; j++) {
        ctx.beginPath();
        ctx.moveTo(plotx[j],ploty[j]);
        ctx.lineTo(plotx[j+1],ploty[j+1]);
        ctx.stroke();
      }
      ctx.lineTo(plotx[0],ploty[0]);
      ctx.stroke();
      for(k = 0; k < plotx.length; k++){
        ctx.fillRect(plotx[k]-pt_size,ploty[k]-pt_size,2*pt_size,2*pt_size);
      }
    }
  }

  this.mouseup = function() {
    disableButtons();
    if(is_close_to_start()){
      if (x.length<3) {
        alert("Polygon must have at least three points")
      } else {
        this.data[0].push(x);
        this.data[1].push(y);
        reset();
      }
    } else{
      var xy = grab_xy(event) 
      x[numpts] = xy[0];
      y[numpts] = xy[1];
      numpts = numpts + 1;
      draw_canvas();
    }
  }

  this.deleteOne = function() {
    if (this.data[0].length > 0) {
      this.data[0].pop();
      this.data[1].pop();
      draw_canvas();
    }
  }

}

var lineObj = function(name, type) {
  this.name = name;
  this.type = type;
  this.data = [new Array(), new Array()];

  this.draw = function() {
    thisx = this.data[0];
    thisy = this.data[1];
    tp = thisx.length;
    for(i = 0; i < tp; i++) {
      plotx = thisx[i];
      ploty = thisy[i];
      for (j = 0; j< plotx.length; j++) {
        ctx.beginPath();
        ctx.moveTo(plotx[j],ploty[j]);
        ctx.lineTo(plotx[j+1],ploty[j+1]);
        ctx.stroke();
      }
      for(k = 0; k < plotx.length; k++){
        ctx.fillRect(plotx[k]-pt_size,ploty[k]-pt_size,2*pt_size,2*pt_size);
      }
    }
    
  }

  this.mouseup = function() {
    disableButtons();
    var xy = grab_xy(event) 
    x[numpts] = xy[0];
    y[numpts] = xy[1];
    numpts = numpts + 1;
    draw_canvas(); 
  }

  this.save = function() {
    if (x.length<2) {
      alert("Lines must be at least two points long")
    } else {
      this.data[0].push(x);
      this.data[1].push(y);
      reset();
      draw_canvas();
    }
    
  }

  this.deleteOne = function() {
    if (this.data[0].length > 0) {
      this.data[0].pop();
      this.data[1].pop();
      draw_canvas();
    }
  }
}

var pointObj = function(name, type) {
  this.name = name;
  this.type = type;
  this.data = [new Array, new Array];

  this.draw = function() {
    lx = this.data[0];
    ly = this.data[1];
    for (i = 0; i < lx.length; i++){
       ctx.fillRect(lx[i]-5, ly[i]-5, 10, 10);
    }
  }
  this.mouseup = function() {
    var xy = grab_xy(event);
    this.data[0].push(xy[0]);
    this.data[1].push(xy[1]);
    draw_canvas();
  }

  this.deleteOne = function() {
    if (this.data[0].length > 0) {
      this.data[0].pop();
      this.data[1].pop();
      draw_canvas();
    }
  }
  
}


function isFunction(functionToCheck) {
  var getType = {};
  return functionToCheck && getType.toString.call(functionToCheck) === '[object Function]';
}

var thisFile;

//polygon coordinates
var x = new Array();
var y = new Array();

//current location
var cx=0;
var cy=0;

var numpts=0;

//tolerance radius
var tr=5;

//drawing styles
var currentColor = ['cyan', 'red'];
var linewidth = 4.0;
var pt_size   = 4.0;
var pt_color  = "black";

// index of the point selected
// var selected_idx = -1;


// top level initialization of the canvas given an image name
function init_canvas(){
  thisFile = new fullFile();

  img = new Image();
  
  var avColors = JSON.parse(colors);
  dotColors = avColors['dotcolors'];
  lineColors = avColors['linecolors'];

  // tokenize the category and image name based on a +
  var cat_img_name = get_category_image_name();
  var tokens = cat_img_name.split('+');
  category_name = tokens[0];
  image_name    = tokens[IMG_COUNT+1];

  // Get the things which we are annotating for
  var annTypes = JSON.parse(fileTypes);
  var ann_names = get_annotation_names();
  var anns = ann_names.split('+');
  for (i = 0; i < anns.length; i++) {
    var name = anns[i];
    var type = annTypes[0][name]
    console.log(annTypes);
    if (!(name in annTypes[0])) {
      console.log(name + ' does not exist')
    }
    var newObj; 
    switch (type) {
      case 'polygon':
        newObj = new polyObj(name, type);
        break;
      case 'line':
        newObj = new lineObj(name, type);
        break;
      case 'point':
        newObj = new pointObj(name, type);
        break;
      default:
        console.log("Type does not exist")
    }
    thisFile.objs.push(newObj);
    thisFile.annotations.push(name);
    for (var property in newObj) {
      if (newObj.hasOwnProperty(property)) {
          if (isFunction(newObj[property])){
            newObj[property] = newObj[property].bind(newObj); 
            // Binds all functions inside annotation objects so that "this" inside those functions refers to the larger object
            // Now, methods inside the object def work like methods do for objects in java
          }
      }
    }

    // Set up Submit Button
    numImgsToGo = get_category_image_name().split('+').length-2
    if (numImgsToGo != 0) {
      $('#submitButton').prop('value','Next Image (' + numImgsToGo + ' More)')
    } else {
      $('#submitButton').prop('value','Submit Results')
    }
    
  }

  //construct the image source from the url parameters 
  img.src = base_url + '/images/' + category_name + '/' + image_name;
  thisFile.fileName = category_name+"/"+image_name; 
  canvas_fix = document.getElementById("segmentation_canvas");
  table = document.getElementById("tbl")
  document.getElementById("instructions").action = "instructions.html?category-name="+cat_img_name;
  ctx = canvas_fix.getContext("2d");
  canvas_fix.onmousemove = mousemove_canvas;
  canvas_fix.onmousedown = mousedown_canvas;
  img.onload = draw_image;
  draw_canvas();
}
// draw canvas
function draw_canvas(){
  // Draw image, then each object type's draw method, then all current points
  ctx.clearRect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT);
  draw_image();
  for (ind = 0; ind < thisFile.objs.length; ind++) {
    ctx.strokeStyle = lineColors[ind];
    ctx.fillStyle = dotColors[ind];
    ctx.lineWidth = linewidth;
    thisFile.objs[ind].draw();
  }
  draw_current();
}

// fix this - wait to draw the image (see if this really works)
function draw_image(){
  ctx.drawImage(img,0,0,CANVAS_WIDTH, CANVAS_HEIGHT);
}

// draw the current point
function draw_current_point(r){
  ctx.fillRect(cx-r,cy-r,2*r,2*r);
}


// draw the series of points the person is working on right now, be it polygon or line
function draw_current() {
  if(x.length > 0){
    ctx.strokeStyle = currentColor[0];
    ctx.fillStyle = currentColor[1];
    ctx.lineWidth = linewidth;
    ctx.beginPath();
    for(i = 0; i < x.length-1; i++){
      ctx.moveTo(x[i],y[i]);
      ctx.lineTo(x[i+1],y[i+1]);
      ctx.stroke();
    }

    ctx.moveTo(x[numpts-1],y[numpts-1]);
    ctx.lineTo(cx,cy); // the current location
    ctx.stroke();
    for(i = 0; i < numpts; i++){
      ctx.fillRect(x[i]-pt_size,y[i]-pt_size,2*pt_size,2*pt_size);
    }
    if(is_close_to_start())
      draw_current_point(2*pt_size);
    else
      draw_current_point(pt_size);
  }
}

// Reset current annotation
function reset() {
  x = new Array();
  y = new Array();
  numpts = 0;
  enableButtons();
}

function setUp() {
  var selected = $('input[name=radbutton]:checked').val();
  var index = thisFile.annotations.indexOf(selected);
  workingObj = thisFile.objs[index];
  if (workingObj != undefined) {
    canvas_fix.onmouseup = workingObj.mouseup;
    console.log(workingObj.name)
  }
  console.log("past mouseup")
}
//Settings for line or polygon or annotation


function mousedown_canvas(event){
  selected_idx = get_closest_point_idx();

}
//update the current location of the keypoint
function mousemove_canvas(event){
  var xy = grab_xy(event);
  cx = xy[0];
  cy = xy[1];
  draw_canvas();
}

//keys to reset the annotation
function keydown(event) {
  var key = String.fromCharCode(event.keyCode || event.which);
  key = key.toUpperCase();
  var indc = 0;
  console.log("Quitting one");
  switch (key) {
      case "C":
        reset(); 
        break;

      case "L":
        if (workingObj.type=='line') {
          workingObj.save();
        }
        break;
  }

  for (indc = 0; indc < annotations.length; indc++) {
    if (quitString.substring(indc,indc+1) == key) {
      thisFile.objs[indc].deleteOne();
      break;
    }
    
  }

  draw_canvas();
}

function disableButtons(){
  allButtons = document.getElementsByName('radbutton');
  for (var i=0; i<allButtons.length;i++){
    allButtons[i].disabled=true;
  }
}

function enableButtons() {
  allButtons = document.getElementsByName('radbutton');
  for (var i=0; i<allButtons.length;i++){
    allButtons[i].disabled=false;
  }
}

// true if the point is close to the start
function is_close_to_start(){
  if(numpts > 0){
    var d2 = (cx-x[0])*(cx-x[0]) + (cy-y[0])*(cy-y[0]);
    return d2 < tr*tr;
  }else{
    return false;
  }
}
// returns the index of the point close to the current one (within tr)
function get_closest_point_idx(){
  var idx = -1;
  var min_dist = 100000000;
  for(var i=0;i<numpts;i++){
    var d2 = (cx-x[i])*(cx-x[i]) + (cy-y[i])*(cy-y[i]);
    if(d2 < min_dist){
      min_dist = d2;
      idx = i;
    }
  }
  if(min_dist < tr*tr)
    return idx;
  else
    return -1;
}

                        
// GUI input handling
function grab_xy(event){
  var ev = event || window.event;
  
  var IE = document.all?true:false;
  if (IE) { // grab the x-y pos if browser is IE
    cx = ev.clientX + document.body.scrollLeft;
    cy = ev.clientY + document.body.scrollTop;
  }
  else {  // grab the x-y pos if browser is NS
    cx = ev.pageX;
    cy = ev.pageY;
  }  
  cx = cx - canvas_fix.offsetLeft- table.offsetLeft;
  cy = cy - canvas_fix.offsetTop - table.offsetTop;
  if (cx < 0){cx = 0;}
  if (cy < 0){cy = 0;}
  if (cx > CANVAS_WIDTH) {cx = CANVAS_WIDTH};
  if (cy > CANVAS_HEIGHT){cy = CANVAS_HEIGHT};
    
  return [cx,cy];
}

// functions related to AMT task
function gup(name){
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var tmpURL = window.location.href;
  var results = regex.exec( tmpURL );
  if( results == null )
    return "";
  else
    return results[1];
}

function convertDataRecurse(arr, multVal, i) {
  if (arr.constructor!= Array) {
    console.log(arr);
    console.log("is number");
    return Math.round(arr * multVal);
  }
  else {
    console.log(arr);
    console.log("is Array");
    while (i<arr.length) {
      arr[i] = convertDataRecurse(arr[i], multVal, 0);
      i++;
    }
    return arr;
  }
}

// Transform data to be terms of original image coordinates
function convertData(){
  for (a = 0; a < thisFile.objs.length; a++) {
    toConvert = thisFile.objs[a];
    toConvert.data[0] = convertDataRecurse(toConvert.data[0], img.width / CANVAS_WIDTH, 0);
    console.log("switching from x to y");
    toConvert.data[1] = convertDataRecurse(toConvert.data[1], img.height / CANVAS_HEIGHT, 0);
    console.log(toConvert.name)
  }
}

// grab the results and submit to the server
function submitResults(){
  if(!x.length==0){
    alert("Please close the polygon before submitting.");
    return;
  }
  convertData();
  var results = JSON.stringify(thisFile);
  RESULT_STRING += results + "\n"
  console.log(RESULT_STRING)
  numImgsToGo = get_category_image_name().split('+').length-IMG_COUNT-2
  console.log("Num To Go:" + numImgsToGo)
  if (numImgsToGo<=0){
    document.getElementById('segpoly').value = RESULT_STRING;
    console.log(RESULT_STRING);
    document.forms["mturk_form"].submit();
  } else {
    IMG_COUNT ++
    console.log('Img Count: ' + IMG_COUNT)
    init_canvas()
    setUp()
  }
  numImgsToGo = get_category_image_name().split('+').length-IMG_COUNT-2
  if (numImgsToGo >0){
    $('#submitButton').prop('value','Next Image (' + numImgsToGo + ' More)')
  } else {
    $('#submitButton').prop('value','Submit Results')
  }
  

}

function get_category_image_name(){
  var cat_img_name = gup('category-image');
  if(cat_img_name == "")
    cat_img_name = "stock+oops.png";
  return cat_img_name;
}

function get_annotation_names() {
  annString = gup('annotation');
  annString = decodeURIComponent(annString);
  if (annString == "") {
    annString = "building+road+lampPost"
  }
  return annString;
}