class IssueController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit]
  def index
    def get_issue_from_title(title)
      title=title.gsub('-',' ').gsub('_',' ')
      Issue.limit(1).where("title like ?", "%#{title}%").first
    end

    @issue=get_issue_from_title(params[:issue_title])
    raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
  end

  def new
  end

  def edit
    @issues=Issue.all()
  end
end
