class AdminController < ApplicationController
  before_filter :authenticate_admin!
  layout "admin"
  def index
  end
  def issues
    @issues=Issue.order(:number)
  end
  def authors
    @authors=Author.order(:last_name,:first_name)
  end
end
