class IssuesController < ApplicationController
  def index
  end

  def new
  end

  def edit
    @issues=Issues.all()
  end
end
