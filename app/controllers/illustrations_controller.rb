class IllustrationsController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:update,:all]
  def show
    @illustration=Illustration.find(params[:id])
  end

  def new
    @illustration=Illustration.new
    @pieces=Piece.find(:all, :order => "issue_id, title")
    @authors=Author.find(:all, :order => "last_name, first_name")
  end
  def create
    # TODO - allow uploading
    params[:illustration][:issue_id] = Piece.find(params[:illustration][:piece_id]).issue.id
    illustration=Illustration.new(params[:illustration])
    saved = illustration.save()
    if saved      
      illustration.piece.add_illustration_content(illustration)
      redirect_to :controller=>'pieces', :action => 'show', :id=>illustration.piece.id
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
    illustration=Illustration.find(params[:id])
    params[:illustration][:issue_id] = Piece.find(params[:illustration][:piece_id]).issue.id
    saved=illustration.update_attributes(params[:illustration])
    if saved
      illustration.piece.add_illustration_content(illustration)
      redirect_to "/pieces/#{illustration.piece.id}"
    else
      redirect_to "/illustrations/#{illustration.id}/edit"
    end
    
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
