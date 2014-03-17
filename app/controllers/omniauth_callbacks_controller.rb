class OmniauthCallbacksController < Devise::OmniauthCallbacksController
  def google_oauth2
    user = Admin.from_omniauth(request.env["omniauth.auth"])
    if user.persisted?
      flash.notice = "Signed in Through Google!"
      sign_in_and_redirect user
    end
    # otherwise fails with error
  end
end