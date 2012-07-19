class PiecesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy]
  def index
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
  
end
