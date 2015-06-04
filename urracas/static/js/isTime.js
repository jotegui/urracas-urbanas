/**************************************
 Name: IsTime Function
 Description:This is a function that is similar to the IsDate function in VBScript, but this function checks for 3 Valid Time Formats and returns true or false.
 By: Randy McCleary

 Inputs:Time in the following formats:
 hh:mm:ss tt - 2:30:00 PM
 hh:mm tt - 2:30 PM
 hh:mm- 4:30

 Returns:true or false

 This code is copyrighted and has
 limited warranties.Please see http://www.Planet-Source-Code.com/vb/scripts/ShowCode.asp?txtCodeId=3638&lngWId=14
 for details.

 IsTime: Returns a Boolean (true) if the Time is validated as a 
 Time Format, false is not
 Parameters:
strTime: String Time in following formats:
		hh:mm:ss tt - 3:48:01 PM
		hh:mm tt- 3:48 PM
		hh:mm- 15:48
 Returns: Boolean
***************************************************************/
function IsTime(strTime) {
	var strTime1 = /^(\d{1,2})(\:)(\d{2})\2(\d{2})(\ )\w[AM|PM|am|pm]$/;
	var strTime2 = /^(\d{1,2})(\:)(\d{2})(\ )\w[A|P|a|p]\w[M|m]$/;
	var strTime3 = /^(\d{1,2})(\:)(\d{1,2})$/;
	
	var strFormat1 = strTime.match(strTime1);
	var strFormat2 = strTime.match(strTime2);
	var strFormat3 = strTime.match(strTime3);
// Check to see if it matches one of the 3 Format Strings.
	if (strFormat1 == null && strFormat2 == null && strFormat3 == null) {
		return false;
	}
	else if (strFormat1 != null) {
		// Validate for this format: 3:48:01 PM
		if (strFormat1[1] > 12 || strFormat1[1] < 00) {
			return false;
		}
		if (strFormat1[3] > 59 || strFormat1[3] < 00) {
			return false;	
		}
		if (strFormat1[4] > 59 || strFormat1[4] < 00) {
			return false;	
		}
	}
	else if (strFormat2 != null) {
		// Validate for this format: 3:48 PM
		if (strFormat2[1] > 12 || strFormat2[1] < 00) {
			return false;
		}
		if (strFormat2[3] > 59 || strFormat2[3] < 00) {
			return false;	
		}
	}
	else if (strFormat3 != null) {
		// Validate for this format: 15:48
		if (strFormat3[1] > 23 || strFormat3[1] < 00) {
			return false;
		}
		if (strFormat3[3] > 59 || strFormat3[3] < 00) {
			return false;	
		}
	}
	return true;
}
