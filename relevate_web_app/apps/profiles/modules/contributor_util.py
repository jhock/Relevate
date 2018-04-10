from ..models.user_models import UserProfile
from ..models.contributor_model import ContributorProfile, AcademicProfile, ContributorCertification, Degree, OrganizationalAffiliation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from ..modules.important_variables import DELIMETER_FOR_TABLES, DELIMETER_FOR_TABLES_LIST, DEGREE_RANKING_DIC
from ..models.contributor_model import AcademicProfileUnfinished, OrganizationalAffiliationUnfinished, ContributorCertificationUnfinished



def user_can_contribute(user):
	'''
	Checks if user is a valid contributor

	:param user: A User model object
	:return: A contributor instance object if user can contribute. Returns False if they can't
	'''
	try:
		user_profile = UserProfile.objects.get(user=user)
		contributor_profile = ContributorProfile.objects.get(user_profile=user_profile, is_approved=True)
		return contributor_profile
	except ObjectDoesNotExist:
		print ("RIGHT HERE")
		return  None


def has_adviser(contributor):
	if contributor.advisers_profile:
		return contributor.advisers_profile
	else:
		return False


def validate_academic_and_cert(academics_req, request):
	'''
	Checks to make sure user has entered valid academic credentials

	:param request: Django's request object for setting up the message warning

	:param academics_req: A list of academic credential gotten from user's input

	:return: True or False based on whether list is empty or not
	'''
	if academics_req:
		return True
	else:
		messages.warning(request, 'Make sure you have at least one academic qualification listed!')
		return False


def get_contributor_credentials(contributor_profile):
	"""
	Gets contributors credentials

	:param contributor_profiles: the contributor profile

	:returns: a dictionary of contributor academic profiles and certifications
	"""
	academic_list = AcademicProfile.objects.filter(contributor_profile=contributor_profile)
	certificate_list = ContributorCertification.objects.filter(contributor_profile=contributor_profile)
	cred_dic = {
		'academic_profile':academic_list,
		'certifications': certificate_list
	}
	return cred_dic


def get_list_of_contributor_credentials(contributor_profile_list):
	"""
	A list of contributors profiles

	:param contributor_profile_list: a list of contributor profile model objects

	:returns: a list of dictionaries represent contributors personal information, slug field and credentials
	"""
	credentials_list = []
	for each_contrib in contributor_profile_list:
		credentials = get_contributor_credentials(each_contrib)
		contrib_prof = {
			'credentials': credentials,
			'first_name':each_contrib.user_profile.user.first_name,
			'last_name':each_contrib.user_profile.user.last_name,
			'id':each_contrib.id
		}
		credentials_list.append(contrib_prof)
	return credentials_list


def update_contributor_qualification(academics_req, cert_req, org_req, contributor_profile, update=True):
	"""
	updates a contributor's academic and certification profile upon update and create

	:param academics_req:  list of academic profile created by the user

	:param cert_req:  list of certifcations created by the user

	:param contributor_profile: user's contribution profile

	:param update: this parameter is true if the update is editing current profile and is false if it is creating a new one

	"""
	if update:
		academic_list = AcademicProfile.objects.filter(contributor_profile=contributor_profile)
		certificate_list = ContributorCertification.objects.filter(contributor_profile=contributor_profile)
		organizational_affiliation_list = OrganizationalAffiliation.objects.filter(contributor_profile=contributor_profile)
		for qual in academic_list:
			qual.delete()

		for cert_qual in certificate_list:
			print("cert is being deleted ")
			cert_qual.delete()
		for org_qual in organizational_affiliation_list:
			print("org is being deleted ")
			org_qual.delete()
	academics_dic = convert_academic_req_to_dic(academics_req)
	cert_dic = convert_certificate_req_to_dic(cert_req)
	affiliation_dic = convert_affiliation_req_to_dic(org_req)
	for item in academics_dic:
		print(academics_dic)
		degree = Degree.objects.filter(name=item['degree']).first()
		program = item['program']
		institution = item['institute']
		new_qualification = AcademicProfile(degree=degree, program=program,
											institution=institution, contributor_profile=contributor_profile)
		new_qualification.save()
	for item in cert_dic:
		name_of_certification = item['program']
		cert_qualification = ContributorCertification(name_of_certification=name_of_certification,
											contributor_profile=contributor_profile)
		cert_qualification.save()
	for item in affiliation_dic:
		name_of_affiliation = item['affiliation']
		affiliation_qualification = OrganizationalAffiliation(name_of_affiliation=name_of_affiliation, contributor_profile=contributor_profile)

		affiliation_qualification.save()

def unfinished_contributor_qualification(academics_req, cert_req, org_req, contributor_profile):
	"""
	updates a contributor's academic and certification profile upon update and create

	:param academics_req:  list of academic profile created by the user

	:param cert_req:  list of certifcations created by the user

	:param contributor_profile: user's contribution profile

	:param update: this parameter is true if the update is editing current profile and is false if it is creating a new one

	"""
	if academics_req:
		academics_dic = convert_academic_req_to_dic(academics_req)
		for item in academics_dic:
			print(academics_dic)
			degree = Degree.objects.get(name=item['degree'])
			program = item['program']
			institution = item['institute']
			new_qualification = AcademicProfileUnfinished(degree=degree, program=program,
												institution=institution, contributor_profile=contributor_profile)
			new_qualification.save()
	if cert_req:
		cert_dic = convert_certificate_req_to_dic(cert_req)
		for item in cert_dic:
			name_of_certification = item['program']
			cert_qualification = ContributorCertificationUnfinished(name_of_certification=name_of_certification,
												contributor_profile=contributor_profile)
			cert_qualification.save()
	if org_req:
		affiliation_dic = convert_affiliation_req_to_dic(org_req)
		for item in affiliation_dic:
			name_of_affiliation = item['affiliation']
			affiliation_qualification = OrganizationalAffiliationUnfinished(name_of_affiliation=name_of_affiliation, contributor_profile=contributor_profile)
			affiliation_qualification.save()


def convert_academic_req_to_dic(academics_request):
	"""
	Converts html table to python dictionary for academic profile

	:param academics_request: string data from html table created by user

	:returns: python dictionary list of created academic profile
	"""
	academics_request = academics_request.split(DELIMETER_FOR_TABLES_LIST)
	aca_list = []

	for item in academics_request:
		row_dic = {}
		row_items = item.split(DELIMETER_FOR_TABLES)
		row_dic["institute"] = row_items[0]
		row_dic["degree"] = row_items[1]
		row_dic["program"] = row_items[2]
		aca_list.append(row_dic)
	return aca_list


def convert_certificate_req_to_dic(cert_req):
	"""
	Convert html table to python dictionary for certificate request

	:param cert_req: string data from html table created by user

	:returns: python dictionary of created certificates
	"""
	aca_list = []
	if len(cert_req) > 0:
		cert_request = cert_req.split(DELIMETER_FOR_TABLES_LIST)
		for item in cert_request:
			row_dic = {}
			row_dic["program"] = item
			aca_list.append(row_dic)
	return aca_list

def convert_affiliation_req_to_dic(affiliation_req):
	"""
	Convert html table to python dictionary for certificate request

	:param cert_req: string data from html table created by user

	:returns: python dictionary of created certificates
	"""
	aca_list = []
	if len(affiliation_req) > 0:
		affiliation_request = affiliation_req.split(DELIMETER_FOR_TABLES_LIST)
		for item in affiliation_request:
			row_dic = {}
			row_dic["affiliation"] = item
			aca_list.append(row_dic)
	return aca_list


def get_max_academic_id(academic_profiles):
	"""
	Returns the Maximum id number for academic profile.
	This enables a starting point number for assigning unique table row id.
	Which we then increment from as user add's and deletes table row

	:param academic_profiles: list of user academic profile

	:returns int value of maximum id. return zero is there exist no academic profile object
	"""
	try:
		id_num = academic_profiles.order_by('-id')[0].id
		return id_num
	except:
		return 0


def get_max_certificate_id(certifications):
	"""
	Returns the Maximum id number from certification model.
	This enables a starting point number for assigning unique table row id.
	Which we then increment from as user add's and deletes table row

	:param certifications: list of users certifications
	
	:returns: int value of maximum id. return zero is there exist no certification object
	"""
	try:
		id_num = certifications.order_by('-id')[0].id
		return id_num
	except:
		return 0


def get_max_affiliation_id(organizational_affiliations):
	"""
	Returns the Maximum id number from organizational affiliations model.
	This enables a starting point number for assigning unique table row id.
	Which we then increment from as user add's and deletes table row

	:param certifications: list of users organizational affiliations

	:returns: int value of maximum id. return zero is there exist no affiliation object
	"""
	try:
		id_num = organizational_affiliations.order_by('-id')[0].id
		return id_num
	except:
		return 0


def get_contributor_highest_degree(academic_list):
	"""
	Grabs the highest ranking degree of the contributor

	:param contributor: A list of contributor academic profile

	:returns: the academic profile of the highest ranking degree of the user
	"""
	if academic_list:
		latest_rank = 0
		curr_cred = academic_list[0]
		for each_crd in academic_list:
			new_rank = DEGREE_RANKING_DIC[each_crd.degree.abbreviation]
			if new_rank > latest_rank:
				latest_rank = new_rank
				curr_cred = each_crd
		return curr_cred
	return None




def get_states():
	return [
		("Alabama", "Alabama"),
		("Alaska", "Alaska"),
		("Arizona", "Arizona"),
		("Arkansas", "Arkansas"),
		("California", "California"),
		("Colorado", "Colorado"),
		("Connecticut", "Connecticut"),
		("Delaware", "Delaware"),
		("Florida", "Florida"),
		("Georgia", "Georgia"),
		("Hawaii", "Hawaii"),
		("Idaho", "Idaho"),
		("Illinois", "Illinois"),
		("Indiana", "Indiana"),
		("Iowa", "Iowa"),
		("Kansas", "Kansas"),
		("Kentucky", "Kentucky"),
		("Louisiana", "Louisiana"),
		("Maine", "Maine"),
		("Maryland", "Maryland"),
		("Massachusetts", "Massachusetts"),
		("Michigan", "Michigan"),
		("Minnesota", "Minnesota"),
		("Mississippi", "Mississippi"),
		("Missouri", "Missouri"),
		("Montana", "Montana"),
		("Nebraska", "Nebraska"),
		("Nevada", "Nevada"),
		("New Hampshire", "New Hampshire"),
		("New Jersey", "New Jersey"),
		("New Mexico", "New Mexico"),
		("New York", "New York"),
		("North Carolina", "North Carolina"),
		("North Dakota", "North Dakota"),
		("Ohio", "Ohio"),
		("Oklahoma", "Oklahoma"),
		("Oregon", "Oregon"),
		("Pennsylvania", "Pennsylvania"),
		("Rhode Island", "Rhode Island"),
		("South Carolina", "South Carolina"),
		("South Dakota", "South Dakota"),
		("Tennessee", "Tennessee"),
		("Texas", "Texas"),
		("Utah", "Utah"),
		("Vermont", "Vermont"),
		("Virginia", "Virginia"),
		("Washington", "Washington"),
		("West Virginia", "West Virginia"),
		("Wisconsin", "Wisconsin"),
		("Wyoming", "Wyoming"),
		("None", "None")
	]

def get_countries():
	return [("AF", "Afghanistan"),(
"AX", "Aland Islands"),(
"AL", "Albania"),(
"DZ", "Algeria"),(
"AS", "American Samoa"),(
"AD", "Andorra"),(
"AO", "Angola"),(
"AI", "Anguilla"),(
"AQ", "Antarctica"),(
"AG", "Antigua and Barbuda"),(
"AR", "Argentina"),(
"AM", "Armenia"),(
"AW", "Aruba"),(
"AU", "Australia"),(
"AT", "Austria"),(
"AZ", "Azerbaijan"),(
"BS", "Bahamas"),(
"BH", "Bahrain"),(
"BD", "Bangladesh"),(
"BB", "Barbados"),(
"BY", "Belarus"),(
"BE", "Belgium"),(
"BZ", "Belize"),(
"BJ", "Benin"),(
"BM", "Bermuda"),(
"BT", "Bhutan"),(
"BO", "Bolivia"),(
"BQ", "Bonaire"),(
"BA", "Bosnia and Herzegovina"),(
"BW", "Botswana"),(
"BV", "Bouvet Island"),(
"BR", "Brazil"),(
"IO", "British Indian Ocean Territory"),(
"BN", "Brunei Darussalam"),(
"BG", "Bulgaria"),(
"BF", "Burkina Faso"),(
"BI", "Burundi"),(
"KH", "Cambodia"),(
"CM", "Cameroon"),(
"CA", "Canada"),(
"CV", "Cape Verde"),(
"KY", "Cayman Islands"),(
"CF", "Central African Republic"),(
"TD", "Chad"),(
"CL", "Chile"),(
"CN", "China"),(
"CX", "Christmas Island"),(
"CC", "Cocos (Keeling) Islands"),(
"CO", "Colombia"),(
"KM", "Comoros"),(
"CG", "Congo"),(
"CD", "The Democratic Republic of the Congo"),(
"CK", "Cook Islands"),(
"CR", "Costa Rica"),(
"CI", "Cote d'Ivoire"),(
"HR", "Croatia"),(
"CU", "Cuba"),(
"CW", "Curacao"),(
"CY", "Cyprus"),(
"CZ", "Czech Republic"),(
"DK", "Denmark"),(
"DJ", "Djibouti"),(
"DM", "Dominica"),(
"DO", "Dominican Republic"),(
"EC", "Ecuador"),(
"EG", "Egypt"),(
"SV", "El Salvador"),(
"GQ", "Equatorial Guinea"),(
"ER", "Eritrea"),(
"EE", "Estonia"),(
"ET", "Ethiopia"),(
"FK", "Falkland Islands (Malvinas)"),(
"FO", "Faroe Islands"),(
"FJ", "Fiji"),(
"FI", "Finland"),(
"FR", "France"),(
"GF", "French Guiana"),(
"PF", "French Polynesia"),(
"TF", "French Southern Territories"),(
"GA", "Gabon"),(
"GM", "Gambia"),(
"GE", "Georgia"),(
"DE", "Germany"),(
"GH", "Ghana"),(
"GI", "Gibraltar"),(
"GR", "Greece"),(
"GL", "Greenland"),(
"GD", "Grenada"),(
"GP", "Guadeloupe"),(
"GU", "Guam"),(
"GT", "Guatemala"),(
"GG", "Guernsey"),(
"GN", "Guinea"),(
"GW", "Guinea-Bissau"),(
"GY", "Guyana"),(
"HT", "Haiti"),(
"HM", "Heard Island and McDonald Islands"),(
"VA", "Holy See (Vatican City State)"),(
"HN", "Honduras"),(
"HK", "Hong Kong"),(
"HU", "Hungary"),(
"IS", "Iceland"),(
"IN", "India"),(
"ID", "Indonesia"),(
"IR", "Islamic Republic of Iran"),(
"IQ", "Iraq"),(
"IE", "Ireland"),(
"IM", "Isle of Man"),(
"IL", "Israel"),(
"IT", "Italy"),(
"JM", "Jamaica"),(
"JP", "Japan"),(
"JE", "Jersey"),(
"JO", "Jordan"),(
"KZ", "Kazakhstan"),(
"KE", "Kenya"),(
"KI", "Kiribati"),(
"KP", "Democratic People's Republic of Korea"),(
"KR", "Republic of Korea"),(
"KW", "Kuwait"),(
"KG", "Kyrgyzstan"),(
"LA", "Lao People's Democratic Republic"),(
"LV", "Latvia"),(
"LB", "Lebanon"),(
"LS", "Lesotho"),(
"LR", "Liberia"),(
"LY", "Libya"),(
"LI", "Liechtenstein"),(
"LT", "Lithuania"),(
"LU", "Luxembourg"),(
"MO", "Macao"),(
"MK", "Republic of Macedonia"),(
"MG", "Madagascar"),(
"MW", "Malawi"),(
"MY", "Malaysia"),(
"MV", "Maldives"),(
"ML", "Mali"),(
"MT", "Malta"),(
"MH", "Marshall Islands"),(
"MQ", "Martinique"),(
"MR", "Mauritania"),(
"MU", "Mauritius"),(
"YT", "Mayotte"),(
"MX", "Mexico"),(
"FM", "Federated States of Micronesia"),(
"MD", "Republic of Moldova"),(
"MC", "Monaco"),(
"MN", "Mongolia"),(
"ME", "Montenegro"),(
"MS", "Montserrat"),(
"MA", "Morocco"),(
"MZ", "Mozambique"),(
"MM", "Myanmar"),(
"NA", "Namibia"),(
"NR", "Nauru"),(
"NP", "Nepal"),(
"NL", "Netherlands"),(
"NC", "New Caledonia"),(
"NZ", "New Zealand"),(
"NI", "Nicaragua"),(
"NE", "Niger"),(
"NG", "Nigeria"),(
"NU", "Niue"),(
"NF", "Norfolk Island"),(
"MP", "Northern Mariana Islands"),(
"NO", "Norway"),(
"OM", "Oman"),(
"PK", "Pakistan"),(
"PW", "Palau"),(
"PS", "Occupied Palestinian Territory"),(
"PA", "Panama"),(
"PG", "Papua New Guinea"),(
"PY", "Paraguay"),(
"PE", "Peru"),(
"PH", "Philippines"),(
"PN", "Pitcairn"),(
"PL", "Poland"),(
"PT", "Portugal"),(
"PR", "Puerto Rico"),(
"QA", "Qatar"),(
"RE", "Reunion"),(
"RO", "Romania"),(
"RU", "Russian Federation"),(
"RW", "Rwanda"),(
"BL", "Saint Barthelemy"),(
"SH", "Saint Helena"),(
"KN", "Saint Kitts and Nevis"),(
"LC", "Saint Lucia"),(
"MF", "Saint Martin"),(
"PM", "Saint Pierre and Miquelon"),(
"VC", "Saint Vincent and the Grenadines"),(
"WS", "Samoa"),(
"SM", "San Marino"),(
"ST", "Sao Tome and Principe"),(
"SA", "Saudi Arabia"),(
"SN", "Senegal"),(
"RS", "Serbia"),(
"SC", "Seychelles"),(
"SL", "Sierra Leone"),(
"SG", "Singapore"),(
"SX", "Sint Maarten (Dutch part)"),(
"SK", "Slovakia"),(
"SI", "Slovenia"),(
"SB", "Solomon Islands"),(
"SO", "Somalia"),(
"ZA", "South Africa"),(
"GS", "South Georgia and the South Sandwich Islands"),(
"ES", "Spain"),(
"LK", "Sri Lanka"),(
"SD", "Sudan"),(
"SR", "Suriname"),(
"SS", "South Sudan"),(
"SJ", "Svalbard and Jan Mayen"),(
"SZ", "Swaziland"),(
"SE", "Sweden"),(
"CH", "Switzerland"),(
"SY", "Syrian Arab Republic"),(
"TW", "Taiwan"),(
"TJ", "Tajikistan"),(
"TZ", "United Republic of Tanzania"),(
"TH", "Thailand"),(
"TL", "Timor-Leste"),(
"TG", "Togo"),(
"TK", "Tokelau"),(
"TO", "Tonga"),(
"TT", "Trinidad and Tobago"),(
"TN", "Tunisia"),(
"TR", "Turkey"),(
"TM", "Turkmenistan"),(
"TC", "Turks and Caicos Islands"),(
"TV", "Tuvalu"),(
"UG", "Uganda"),(
"UA", "Ukraine"),(
"AE", "United Arab Emirates"),(
"GB", "United Kingdom"),(
"US", "United States"),(
"UM", "United States Minor Outlying Islands"),(
"UY", "Uruguay"),(
"UZ", "Uzbekistan"),(
"VU", "Vanuatu"),(
"VE", "Venezuela"),(
"VN", "Viet Nam"),(
"VG", "Virgin Islands, British"),(
"VI", "Virgin Islands, U.S."),(
"WF", "Wallis and Futuna"),(
"EH", "Western Sahara"),(
"YE", "Yemen"),(
"ZM", "Zambia"),(
"ZW", "Zimbabwe")]