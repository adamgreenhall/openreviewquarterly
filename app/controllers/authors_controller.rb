class AuthorsController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy]
  def index
    @author=get_author_from_name(params[:author_name])
    @pieces=@author.pieces.joins(:issue).where({:issues => {:is_published => true}}).sort_by{|p| p.issue.number}.reverse
  end

  def new
    @author=Author.new()
  end

  def edit
    @author=Author.find(params[:author])
  end

  def create
    saved=Author.new(params[:author]).save()
    if saved
      redirect_to '/authors/all'
    else #form had errors
      redirect_to '/authors/new'
    end
  end
  
  def destroy
    Author.find(params[:author]).delete
  end
    
  def all
    @authors=Author.all
  end
  
end
