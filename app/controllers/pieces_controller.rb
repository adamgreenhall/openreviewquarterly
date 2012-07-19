class PiecesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:all]
  def show
    if params[:issue_title]
      @piece=get_piece_from_titles(params)
      raise ActionController::RoutingError.new('Piece not found') if @piece.nil?
    else
      @piece=Piece.find(params[:id])
    end
  end

  def new
    @piece=Piece.new()
  end

  def edit
    @piece=Piece.find(params[:piece])
  end

  def create
    saved=Piece.new(params[:piece]).save()
    if saved
      redirect_to '/pieces/all'
    else #form had errors
      redirect_to '/pieces/new'
    end
  end
  
  def destroy
    Piece.find(params[:piece]).delete
  end
  
  def all
  end
end
