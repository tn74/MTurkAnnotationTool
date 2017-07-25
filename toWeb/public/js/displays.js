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
 
function dispString(todisp) {
	todisp = todisp[0].toUpperCase() + todisp.substring(1);
	dispArr = todisp.split(/(?=[A-Z])/);
	return dispArr.join(" ")
}

// right padding s with c to a total of n chars
function padding_right(s, c, n) {
  if (! s || ! c || s.length >= n) {
    return s;
  }
  var max = (n - s.length)/c.length;
  for (var i = 0; i < max; i++) {
    s += c;
  }
  return s;
}

$("#segmentation_canvas").on("contextmenu",function(){
       console.log("No saving");
       return false; 
    });

annString = gup('annotation'); 
annString = decodeURIComponent(annString)
if (annString == "") {
	annString = "building+road+lampPost"
}
annotations = annString.split('+');


var annTypes = JSON.parse(fileTypes);
var color = JSON.parse(colors);

$('<tr> <td align = "center"> L </td>  <td> to <b>complete your line</b> (when on line mode) </td> </tr>').prependTo('#instructionsTable'); // Piece necessary for instructions table

for (i = 0; i < annotations.length; i++) {
    // Creating Radio Buttons
    ann = annotations[i];
    type = annTypes[0][ann];
    var radString = '<tr> <td width="180"> &nbsp;&nbsp;<input type="radio" name="radbutton" onclick = "setUp()" value = "'+ ann +'"">&nbsp;'+ dispString(ann) +'</td><td width = "100" align = "left"> (' + dispString(type) + ')';
    if (type != 'point') {
      radString = radString + '</td> <td> <div class="foo" style = "background: '+ color['dotcolors'][i] +'"></div></td>' + '<td> <div class="foo" style = "background: '+ color['linecolors'][i] +'"></div> </td>';
    } else {
      radString = radString + '</td> <td> <div class="foo" style = "background: '+ color['dotcolors'][i] +'"></div>  </td>';
    }
    radString += + '</tr>';
    var radioBtn = $(radString);
    radioBtn.appendTo('#RadioButtonTable');


    // Creating Instructions Table
    ann = annotations[annotations.length-1-i];
    type = annTypes[0][ann];

    var instString = '<tr><td align = "center">' + quitString.substring(annotations.length-i-1,annotations.length-i).toUpperCase() + '</td><td > Delete the last <b>'+ dispString(ann) + '</b> </td></tr>';
    var instRow = $(instString);
    instRow.prependTo('#instructionsTable');

    // Creating Table
    
    var newImgText  = '<td width = 170 align = "center"> <img src="images/sample/'+ann+'.png" height="150" width="150"></td>';
    var newImg = $(newImgText);
    newImg.prependTo('#sampleImages');
    
    var newAnnNameText = '<td align = "center"><input type="hidden"/> <a target = _blank" href="helper/'+ann+'.html">' + dispString(ann) + ' </a></td>'
    var newAnnName = $(newAnnNameText);
    newAnnName.prependTo('#annNames');

    var newPolyLabelText = '<td align = "center">' + dispString(type) + ' Tool </td>';
    var newPolyLabel = $(newPolyLabelText);
    newPolyLabel.prependTo('#polyLabels');
}

// Header labels for top instructions panel tables
$('<th width = 100> <center> Sample Image </center> </th>').prependTo('#sampleImages');
$('<th height = 30> <center> Object Name </center> </th>').prependTo('#annNames');
$('<th height = 20> <center> Annotation Tool </center> </th>').prependTo('#polyLabels')
$('<tr> <td align = "center"> C </td>  <td> to clear your current annotations </td> </tr>').prependTo('#instructionsTable');
$('<tr><td align = "center" width = 100 > <b> Use Key </b></th> <th width = 400 align = "center"> To complete the following action </th> </tr>').prependTo('#instructionsTable');
