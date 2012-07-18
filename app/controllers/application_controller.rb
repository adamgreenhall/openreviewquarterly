class ApplicationController < ActionController::Base
  protect_from_forgery
  def get_issue_from_title(title)
    title=title.gsub('-',' ').gsub('_',' ')
    Issue.limit(1).where("title like ?", "%#{title}%").first
  end
end
