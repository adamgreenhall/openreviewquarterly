class IssueController < ApplicationController
  def index
    def get_issue_from_title(title)
      title=title.gsub('-',' ').gsub('_',' ')
      Issue.limit(1).where("title like ?", "%#{title}%").first
    end

    @issue=get_issue_from_title(params[:issue_title])
    raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
  end

  def new
  end

  def edit
    @issues=Issue.all()
  end
end
