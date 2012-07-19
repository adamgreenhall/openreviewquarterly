class ApplicationController < ActionController::Base
  protect_from_forgery
  def get_issue_from_title(title)
    title=title.gsub('-',' ').gsub('_',' ')
    Issue.limit(1).where("title like ?", "%#{title}%").first
  end
  def get_author_from_name(name)
    name=name.gsub('-',' ').gsub('_',' ')
    first,last=name.split
    Author.limit(1).where("first_name like ? OR last_name like ?", "%#{first}%","%#{last}").first
  end

  def get_piece_from_titles(params)
     issue=get_issue_from_title(params[:issue_title])
     title=params[:piece_title].gsub('-',' ').gsub('_',' ')
     issue.pieces.where("title like ?","%#{title}").limit(1).first
  end

end
