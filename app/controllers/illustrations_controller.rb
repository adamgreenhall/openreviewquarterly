class IllustrationsController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:update,:all]
  def show
    @illustration=Illustration.find(params[:id])
  end

  def new
    @illustration=Illustration.new
    @pieces=Piece.all
    @authors=Author.all
  end
  def create
    illustration=Illustration.new(params[:illustration])
    saved = illustration.save()
    if saved
      
      piece = Piece.find(illustration.piece.id)
      
      content = render :partial => 'content', :locals =>{:@illustration=>illustration}
      piece.add_illustration_content(content)
      
      redirect_to :controller=>'issues', :action => 'show', :id=>params[:illustration][:issue_id]
    else #form had errors
      redirect_to :acion=>'new'
    end
  end

  def edit
    @illustration=Illustration.find(params[:id])
    @pieces=Piece.all
    @authors=Author.all    
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
