require 'json'
class IssuesController < ApplicationController
  before_filter :authenticate_admin!, :only => [:new,:edit,:create,:destroy,:update,:all]
  layout :resolve_layout
  def show
    if params[:issue_title]
      @issue=get_issue_from_title(params[:issue_title])
      raise ActionController::RoutingError.new('Issue not found') if @issue.nil?
    else
      @issue=Issue.find(params[:id])
    end
    @pieces = @issue.pieces.where("number IS NOT NULL").order(:number)
    if !@issue.is_published && !admin_signed_in?
      redirect_to '/'
    end
  end

  def secret_preview
    @issue = Issue.where(is_published: false).first
    puts @issue
    @pieces = @issue.pieces.where("number IS NOT NULL").order(:number)
    @hide_admin_banner = true
    render :template => "issues/show"
  end

  def new
    @issue=Issue.new(published: false)
  end

  def edit
    @issue=Issue.find(params[:id])
    @pieces=@issue.pieces.where("number IS NOT NULL").order(:number)
    @illustrations=@issue.illustrations
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
  
  private
  def resolve_layout
    case action_name
    when "new", "create", "edit", "update"
      "admin"
    else
      "application"
    end
  end    
end
