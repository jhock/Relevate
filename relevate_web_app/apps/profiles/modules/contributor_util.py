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
			'avatar_image_url':each_contrib.avatar_image_url,
			'user_profile':each_contrib.user_profile,
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
	return ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

def get_countries():
	return ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa',
					'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda',
					'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
					'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
					'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire', 'Bosnia and Herzegovina',
					'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory',
					'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
					'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic',
					'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia',
					'Comoros', 'Congo', 'The Democratic Republic of the Congo', 'Cook Islands', 'Costa Rica',
					"Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech Republic', 'Denmark',
					'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
					'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)',
					'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia',
					'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar',
					'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea',
					'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)',
					'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia',
					'Islamic Republic of Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica',
					'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Democratic People's Republic of Korea",
					'Republic of Korea', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon',
					'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Republic of Macedonia',
					'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
					'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Federated States of Micronesia', 'Republic of Moldova',
					'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru',
					'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue',
					'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
					'Occupied Palestinian Territory', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines',
					'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation',
					'Rwanda', 'Saint Barthelemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin',
					'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
					'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
					'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
					'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan',
					'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland',
					'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'United Republic of Tanzania', 'Thailand',
					'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
					'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
					'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan',
					'Vanuatu', 'Venezuela', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.',
					'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']








