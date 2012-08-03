class IllustrationsContentController < AbstractController::Base
  include AbstractController::Rendering
  include AbstractController::Layouts
  include AbstractController::Helpers
  include AbstractController::Translation
  include AbstractController::AssetPaths

  # Uncomment if you want to use helpers 
  # defined in ApplicationHelper in your views
  helper ApplicationHelper

  # Make sure your controller can find views
  self.view_paths = "app/views"

  # You can define custom helper methods to be used in views here
  # helper_method :current_admin
  # def current_admin; nil; end

  def content(locals)
    render :partial=>"illustrations/content", :locals=>locals
  end
end