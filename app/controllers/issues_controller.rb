class IssuesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:all]
  def show
    if params[:issue_title]
      @issue=get_issue_from_title(params[:issue_title])
      raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
    else
      @issue=Issue.find(params[:id])
    end
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
  end

  def new
    @issue=Issue.new()
  end

  def edit
    @issue=Issue.find(params[:id])
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
    @illustrations=@issue.pieces.where(:kind=>"illustration")
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
