class HomeController < ApplicationController
  def index
    issues=Issue.where(:is_published=>true).order('number',:reverse=>true)
    @current_issue=issues.first
    @back_issues=issues
  end

  def about
  end

  def next
  end
  
  def tech
  end
  
  def people
    
  end
end
