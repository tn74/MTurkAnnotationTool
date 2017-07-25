var dataTypes = function() {
  this.dotcolors = ["mediumblue", "greenyellow", "brown", "gold", "lightpink"];
  this.linecolors = ["dodgerblue", "green", "burlyWood", "goldenrod", "lightsalmon"];
}

var dT = new dataTypes();
saveString = JSON.stringify(dT)
console.log(saveString)