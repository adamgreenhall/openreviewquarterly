class AuthorController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit]
  def index
  end

  def new
  end

  def edit
  end
end
