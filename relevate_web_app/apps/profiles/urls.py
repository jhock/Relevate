
from django.conf.urls import url
from django.contrib.auth import views as django_auth_views

from .views import authentication_views
from .views import adviser_views
from .views import contributor_views
# All of these will be prefixed by "profile"

urlpatterns = [

	# User Registration/Login
	url(r'registration/', authentication_views.RegisterUserView.as_view(), name='registration'),
	url(r'^login/$', authentication_views.UserLogin,  name='login'),
	url(r'^logged_out/$', django_auth_views.logout, name='logged_out'),
	url(r'inactive-user/', authentication_views.DeactivatedAccountView.as_view(), name='deactivated_account'),
	url(r'confirmation/', authentication_views.ConfirmationView.as_view(), name='confirmation'),
	url(r'user_contributor_question/$', authentication_views.UserContributorQuestionView.as_view(), name='user_contributor_question'),

	# User Password Reset/Change Information
	url(r'reset_done/$', django_auth_views.password_reset_complete, name='password_reset_complete'),
	url(r'password_reset_form/$', django_auth_views.password_reset,{'post_reset_redirect': 'password_reset_done/'},
		name='password_reset_form'),
	url(r'password_reset/password_reset_done/$', django_auth_views.password_reset_done	, name="password_reset_done"),
	url(r'user_update/$', authentication_views.UserUpdateView.as_view(), name="user_update"),
	#url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', authentication_views.PasswordResetConfirmView.as_view(),
	# {'post_reset_redirect': 'password_done/'}, name='password_reset_confirm'),
	#url(r'password_done/$', authentication_views.password_reset_complete, name='password_reset_complete'),
	#url('^change_information/$', authentication_views.password_change, name='change_information'),

	# Advisers
	url(r'advisers/', adviser_views.AdviserListView.as_view(), name='advisers'),
	url(r'advisers_create/', adviser_views.AdviserCreateView.as_view(), name='adviser_create'),
	url(r'adviser_profile/', adviser_views.AdviserProfileView.as_view(), name='adviser_profile'),
	url(r'advisers_update/', adviser_views.AdviserUpdateView.as_view(), name='adviser_update'),
	url(r'advisers_approve/', adviser_views.AdviserApproveView.as_view(), name='adviser_approve'),
	url(r'approve_adviser/', adviser_views.ApproveButtonView.as_view(), name='approve_adviser'),
	url(r'deny_adviser/', adviser_views.DenyButtonView.as_view(), name='deny_adviser'),
	url(r'denied_advisers/$', adviser_views.DeniedAdviserListView.as_view(), name="denied_adviser_list"),
	# Adviser Approve Minions Posts 
	url(r'approve-post/$', adviser_views.AdviserApprovePostView.as_view(), name="adviser_approve_posts"),
	url(r'deny-post-ajax/$', adviser_views.DenyPostAjaxView.as_view(), name="deny_post_ajax"),
	url(r'approve-post-ajax/$', adviser_views.ApprovePostAjaxView.as_view(), name="approve_post_ajax"),

	# Contributors
	url(r'contributors/$', contributor_views.ContributorListView.as_view(), name='contributors'),
	url(r'contributors_approve/$', contributor_views.ContributorApproveView.as_view(), name="contributor_approve"),
	url(r'approve_contributor/$', contributor_views.ApproveButtonView.as_view(), name="approve_contributor"),
	url(r'deny_contributor/$', contributor_views.DenyButtonView.as_view(), name="deny_contributor"),
	url(r'request_revison_contributor/$', contributor_views.RequestRevisonButtonView.as_view(), name="request_revison_contributor"),
	url(r'contributors_create/$', contributor_views.ContributorCreateView.as_view(), name="contributor_create"),
	url(r'contributors_temp_save/$', contributor_views.ContributorTempSaveView.as_view(), name="contributor_temp_save"),

	url(r'contributors_update/$', contributor_views.ContributorUpdateView.as_view(), name="contributor_update"),
	url(r'contributor_profile/$', contributor_views.ContributorProfileView.as_view(), name="contributor_profile"),
	url(r'denied_contributors/$', contributor_views.DeniedContributorListView.as_view(), name="denied_contributor_list"),
	url(r'public_contributor/(?P<contrib_id>[\d]+)/$', contributor_views.PublicContributorProfileView.as_view(), name="public_contributor_profile"),
	url(r'^get-university-query/$', contributor_views.QueryUniversities.as_view(), name='query_universities'),

]