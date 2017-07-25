var dataTypes = function() {
  this.road = 'line';
  this.building = 'polygon';
  this.lampPost = 'point';
  this.car = 'point'
}

var dT = new dataTypes();
saveString = JSON.stringify(dT)
console.log(saveString)