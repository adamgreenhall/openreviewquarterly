class HomeController < ApplicationController
  def index
    issues=Issue.all()
    @current_issue = issues.last
    @past_issues = issues
  end

  def about
  end

  def next
  end
end
