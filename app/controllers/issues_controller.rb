class IssuesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:all]
  def index
    @issue=get_issue_from_title(params[:issue_title])
    raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
  end

  def new
    @issue=Issue.new()
  end

  def edit
    @issues=Issue.all()
  end

  def create
    saved=Issue.new(params[:issue]).save()
    if saved
      redirect_to '/issues/all'
    else #form had errors
      redirect_to '/issues/new'
    end
  end
  
  def all
    @issues=Issue.order(:number).all()
  end  
end
