# Shibboleth Configuration

Two choices:
1. Use provided Shibboleth SP (Service Provider)
2. Use 3rd party SAML implementation.

### 1. Native Shibboleth SP implementation
- `mod_shib`: A module for Apache -> need to use Apache as server.
- Tried, tested, maintained, documented.
  - Documented by UofT in terms of configs for production env.
  - Modifications for Django is pretty simple.
- Configs: seems to be a headache.
- As William mentioned, it does seem to be clunky.
  - BUT: Setup seems simple, and involves minimal change to our Django code.
- See: http://www.jeesty.com/shibboleth 

### 2. Using 3rd party SAML implementation
- Would allow us to incorporate at code level.
  - Imports from the python_saml library
- Requires `libssl-dev`, `libxml2-dev`, `libxmlsec1-dev`, `python-dev`
- Requires `pip install requests[security]`
- Not well documented
- See:
  - https://github.com/knaperek/djangosaml2
    - Not well maintained?
    - Is a maintained fork. Original here: https://bitbucket.org/lgs/djangosaml2/overview#rst-header-installation
  - https://github.com/onelogin/python-saml
    - Contains a example django project.

# Shibboleth Connection Flow

A network trace of UofT's shibboleth authentication. User first attempts to
access the **SP** (service provider)'s URL.

1. Client --> SP Shib authenticated URL (Our app, for ex)
  - SP checks if user has session.
    - if not, redirect client to `idp.utorauth.utoronto.ca/...` (*contains a
      SAMLRequest and relay state query string*)
    - **IDP**: Identity provider.

2. Client sends GET to redirect URL (the IDP).
  - IDP returns two cookies, and another redirect.
    - `JSESSIONID`
    - `_idp_authn_lc_key`
    - Redirects to `idp.utorauth.utoronto.ca:443/idp/authengine`

3. Client sends GET to redirect URL.
  - HTML response contains a form, auto submitted using JS.
  - Form contains (already filled by authengine):
    - `pubcookie_g_req`
    - `post_stuff`
    - `relay_url`
  - JS submits the above form to `weblogin.utoronto.ca`

4. Client sends POST triggered by auto-submit form.
  - Displays the UofT web login interface.
  - **USER CLICKS LOG ON**

5. Login click triggers POST to weblogin with user cridentials as form data.
  - Reply: a cookie and another auto-submit form.
    - Cookie: `pubcookie_(...`
    - Auto form (already filled by weblogin):
      - `post_stuff` = "" (empty string)
      - `get_args`
      - `redirect_url`
      - `pub_cookie_g`
    - Submit to: `idp.utorauth.utoronto.ca/PubCookie.reply`

6. Client sends POST triggered by auto-submit form.
  - Reply: cookie `pub_cookie_g` set to value specified within auto-sub form.
  - Redirect back to `/idp/Authn/RemoteUser`

7. Client sends GET to redirect URL.
  - 3 cookies returned, and redirect request received.
  - Sent cookies: `JSESSION`, `_idp_authn_lc_key`, `pubcookie_g`
  - Recieved cookies: `_idp_session`, `pubcookie_g` (delete),
    `pubcookie_s_CIMF_Shibboleth_Pilot`
  - Redirect to `/idp/profile/SAML2/Redirect/SSO`

8. Client sends GET to redirect URL.
  - Reply: an updated `_idp_authn_lc_key`, and an auto-submit form.
  - Form submits:
    - Relay state (same as in step 1)
    - `SAMLResponse`
  - Submit to: `<SP_url>/Shibboleth.sso/SAML2/Post`

9. Client sends POST triggered by auto-submit form.
  - Reply: a cookie (super long name)
    - `_shibsession_64...7468` (http only set to true)
  - Redirect to `<sp_url>/shib/app/sp/sp_request`
  - Is authenticated. SP displays content to user.

#### If session expires:
  - Expiry determined by SP. if expired, return `_shib_session...` cookie within
  expiry, and redo from Step 1.

#### Notes
  - POSTs triggered by auto-submit forms do not send cookies?
  - If user takes too long to log in, weblogin will not reply with an auto-submit
  form, and cause the process to terminate at step 4.
