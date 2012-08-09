class ApplicationController < ActionController::Base
  protect_from_forgery
  def get_issue_from_title(title)
    title=title.split('#').first.gsub('-',' ').gsub('_',' ')
    Issue.limit(1).where("upper(title) like ?", "%#{title.upcase}%").first
  end
  def get_author_from_name(name)
    name=name.gsub('-',' ').gsub('_',' ')
    first,last=name.split
    author=Author.limit(1).where("upper(first_name) like ? AND upper(last_name) like ?", "%#{first.upcase}%","%#{last.upcase}").first
    if author.nil? 
      # try a looser search condition 
      return Author.limit(1).where("upper(first_name) like ? OR upper(last_name) like ?", "%#{first.upcase}%","%#{last.upcase}").first
    else
      return author
    end
  end

  def get_piece_from_titles(params)
     issue=get_issue_from_title(params[:issue_title])
     title=params[:piece_title].gsub('-',' ').gsub('_',' ')
     issue.pieces.where("upper(title) like ?","%#{title.upcase}").limit(1).first
  end

end
