require 'json'
class IssuesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:update,:all]
  def show
    if params[:issue_title]
      @issue=get_issue_from_title(params[:issue_title])
      raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
    else
      @issue=Issue.find(params[:id])
    end
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
    if !@issue.is_published && !admin_signed_in?
      redirect_to '/'
    end
  end

  def new
    @issue=Issue.new()
  end

  def edit
    @issue=Issue.find(params[:id])
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
    @illustrations=@issue.pieces.where(:kind=>"illustration")
  end

  def create
    saved=Issue.new(params[:issue]).save()
    if saved
      redirect_to '/issues/all'
    else #form had errors
      redirect_to '/issues/new'
    end
  end

  def update
    @issue=Issue.find(params[:id])
    piece_order=JSON.parse(params[:issue]['piece_order'])
    params[:issue].delete :piece_order
    
    old_piece_order=@issue.pieces.order(:number).map{|p| p.id}
    if piece_order!=old_piece_order
      piece_order.each_with_index do |id,i|
        Piece.find(id).update_attributes(:number=>i)
      end
    end

    saved=@issue.update_attributes(params[:issue])
    
    if saved
      redirect_to "/issues/#{@issue.id}"
    else
      redirect_to "/issues/#{@issue.id}/edit"
    end
  end

    
  def all
    @issues=Issue.order(:number).all()
  end  
end
