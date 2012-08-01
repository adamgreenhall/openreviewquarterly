class IllustrationsController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:update,:all]
  def show
  end

  def new
    @illustration=Illustration.new
    @pieces=Piece.all
    @authors=Author.all
  end
  def create
    saved=Illustration.new(params[:illustration]).save()
    if saved
      redirect_to :controller=>'issues', :action => 'show', :id=>params[:illustration][:issue_id]
    else #form had errors
      redirect_to :acion=>'new'
    end
  end

  def edit
  end
  def update
  end

  def destroy
    Illustration.find(params[:id]).delete
    respond_to do |format|
      format.html { redirect_to '/' }
      format.js do
        render :nothing => true, :status => :ok
        return true
      end
    end
    
  end


  def all
    @illustrations=Illustration.all()
  end

end
