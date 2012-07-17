class IssueController < ApplicationController
  def index
  end

  def new
  end

  def edit
    @issues=Issue.all()
  end
end
