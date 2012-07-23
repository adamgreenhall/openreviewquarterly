class HomeController < ApplicationController
  def index
    issues=Issue.where(:is_published=>true).order('number').reverse_order
    @current_issue=issues.first
    @back_issues=issues[1..-1]
  end

  def about
  end

  def submit
    @issue=Issue.where(:is_published=>false).order('number').last
  end
  
  def tech
  end
  
  def people
    
  end
end
