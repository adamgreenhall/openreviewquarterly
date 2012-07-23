class AdminController < ApplicationController
  before_filter :authenticate_admin!
  def index
    @authors=Author.order(:last_name,:first_name)
    @issues=Issue.order(:number)
  end
end
