$(document).ready(function()
{
    this.getElementsByClassName('avatar-def').style.backgroundColor = avatarRandomColor();
}


//List of acceptable colors to choose from
var colours = ['#345321', '#888888', '#000011'];

function avatarRandomColor () {
    //Random color for avatar with initials
    var sum = 0;
    var name = this.getElementsByClassName('avatar-def').text
    for (var i = 0; i < name.length; i++){
        sum += name.charAt(i);
        console.log("avatar change");
    }
    return sum % colours.length;
}