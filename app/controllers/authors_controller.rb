class AuthorsController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit]
  def index
    @author=get_author_from_name(params[:author_name])
  end

  def new
  end

  def edit
  end
end
